from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from courses.models import Course

from .forms import AssignmentForm
from .models import Assignment


@login_required
def create_assignment(request, course_id):
    if not request.user.is_faculty:
        raise PermissionDenied

    course = get_object_or_404(
        Course,
        id=course_id,
        faculty=request.user,
    )

    if request.method == "POST":
        form = AssignmentForm(request.POST)

        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.course = course
            assignment.created_by = request.user
            assignment.full_clean()
            assignment.save()

            return redirect("faculty_dashboard")
    else:
        form = AssignmentForm()

    return render(
        request,
        "assignments/create_assignment.html",
        {
            "form": form,
            "course": course,
        },
    )

@login_required
def student_assignments(request):
    if not request.user.is_student:
        raise PermissionDenied

    assignments = (
        Assignment.objects
        .filter(
            course__enrollments__student=request.user,
            is_published=True,
        )
        .select_related("course")
        .order_by("due_date")
    )

    return render(
        request,
        "assignments/student_assignments.html",
        {
            "assignments": assignments,
        },
    )