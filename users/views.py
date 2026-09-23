from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST


from assignments.models import Assignment
from submissions.models import Submission

from .decorators import faculty_required, student_required
from .forms import StudentRegistrationForm


def root_view(request):
    """
    Route root path '/' to dashboard if authenticated,
    or login page if unauthenticated.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    return redirect('login')
def student_register_view(request):
    """
    Register a new Student account.
    """

    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

            return redirect('student_dashboard')
    else:
        form = StudentRegistrationForm()

    return render(
        request,
        'users/student_register.html',
        {
            'form': form,
        },
    )


def login_view(request):
    """
    Handle user login via Django's built-in AuthenticationForm.

    The user must select the correct role:
    STUDENT or FACULTY.

    After successful authentication, the user is redirected
    to the appropriate dashboard.
    """
    if request.user.is_authenticated:
        return redirect('dashboard_redirect')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            selected_role = request.POST.get("role")

            # Validate selected role against the actual user account.
            if selected_role == "STUDENT" and not user.is_student:
                form.add_error(
                    None,
                    "This account is not registered as a Student."
                )

            elif selected_role == "FACULTY" and not user.is_faculty:
                form.add_error(
                    None,
                    "This account is not registered as Faculty."
                )

            elif selected_role not in {"STUDENT", "FACULTY"}:
                form.add_error(
                    None,
                    "Please select a valid role."
                )

            else:
                login(request, user)

                next_url = (
                    request.GET.get('next')
                    or request.POST.get('next')
                )

                if next_url and url_has_allowed_host_and_scheme(
                    next_url,
                    allowed_hosts={request.get_host()}
                ):
                    return redirect(next_url)

                return redirect('dashboard_redirect')

    else:
        form = AuthenticationForm(request)

    return render(
        request,
        'users/login.html',
        {'form': form}
    )


@require_POST
def logout_view(request):
    """
    Handle user logout via POST request only.
    """
    logout(request)
    return redirect('login')


@login_required
def dashboard_redirect_view(request):
    """
    Redirect authenticated user to their role-specific dashboard.
    """
    if request.user.is_student:
        return redirect('student_dashboard')

    elif request.user.is_faculty:
        return redirect('faculty_dashboard')

    raise PermissionDenied(
        "User does not have an assigned role dashboard."
    )


@student_required
def student_dashboard_view(request):
    assignments = (
        Assignment.objects
        .filter(
            course__enrollments__student=request.user,
            is_published=True,
        )
        .select_related("course")
        .order_by("due_date")
    )

    submissions = (
        Submission.objects
        .filter(student=request.user)
        .select_related(
            "assignment",
            "assignment__course"
        )
        .order_by("-submitted_at")
    )

    submitted_assignment_ids = submissions.values_list(
        "assignment_id",
        flat=True,
    )

    current_assignments = (
        assignments
        .filter(due_date__gte=timezone.now())
        .exclude(id__in=submitted_assignment_ids)
    )

    return render(
        request,
        "users/student_dashboard.html",
        {
            "user": request.user,
            "current_assignments": current_assignments,
            "submissions": submissions[:5],
        },
    )


@faculty_required
def faculty_dashboard_view(request):
    """
    Faculty dashboard view.
    """
    assignments = (
        Assignment.objects
        .filter(created_by=request.user)
        .select_related("course")
        .order_by("-created_at")
    )

    return render(
        request,
        "users/faculty_dashboard.html",
        {
            "user": request.user,
            "assignments": assignments,
        },
    )