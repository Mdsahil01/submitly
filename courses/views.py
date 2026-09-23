from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from assignments.models import Assignment

from .forms import CourseForm
from .models import Course, Enrollment
from django.db.models import Prefetch


@login_required
def course_list(request):
    if request.user.is_faculty:
        courses = (
            Course.objects
            .filter(faculty=request.user)
            .order_by("-created_at")
        )

    elif request.user.is_student:
        courses = (
            Course.objects
            .all()
            .prefetch_related(
                Prefetch(
                    "enrollments",
                    queryset=Enrollment.objects.filter(
                        student=request.user
                    ),
                    to_attr="student_enrollments",
                )
            )
            .order_by("-created_at")
        )

    else:
        raise PermissionDenied

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses,
        },
    )

@login_required
def create_course(request):
    if not request.user.is_faculty:
        raise PermissionDenied

    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            course = form.save(commit=False)
            course.faculty = request.user
            course.full_clean()
            course.save()

            return redirect(
                "courses:course_detail",
                course_id=course.id,
            )

    else:
        form = CourseForm()

    return render(
        request,
        "courses/course_create.html",
        {
            "form": form,
        },
    )


@login_required
def course_detail(request, course_id):
    if request.user.is_faculty:
        course = get_object_or_404(
            Course,
            id=course_id,
            faculty=request.user,
        )

    elif request.user.is_student:
        # Student can only open a course after approval.
        enrollment = get_object_or_404(
            Enrollment,
            course_id=course_id,
            student=request.user,
            status="APPROVED",
        )

        course = enrollment.course

    else:
        raise PermissionDenied

    assignments = (
        Assignment.objects
        .filter(course=course)
        .order_by("due_date")
    )

    enrollments = course.enrollments.select_related("student")

    return render(
        request,
        "courses/course_detail.html",
        {
            "course": course,
            "assignments": assignments,
            "enrollments": enrollments,
        },
    )


@login_required
@require_POST
def enroll_course(request, course_id):
    if not request.user.is_student:
        raise PermissionDenied

    course = get_object_or_404(
        Course,
        id=course_id,
    )

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course,
    )

    # If a previous request was rejected, allow the student
    # to request enrollment again.
    if not created and enrollment.status == "REJECTED":
        enrollment.status = "PENDING"
        enrollment.save(update_fields=["status"])

    return redirect("courses:course_list")

@login_required
@require_POST
def approve_enrollment(request, enrollment_id):
    if not request.user.is_faculty:
        raise PermissionDenied

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        course__faculty=request.user,
    )

    enrollment.status = "APPROVED"
    enrollment.save(update_fields=["status"])

    return redirect(
        "courses:course_detail",
        course_id=enrollment.course.id,
    )


@login_required
@require_POST
def reject_enrollment(request, enrollment_id):
    if not request.user.is_faculty:
        raise PermissionDenied

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        course__faculty=request.user,
    )

    enrollment.status = "REJECTED"
    enrollment.save(update_fields=["status"])

    return redirect(
        "courses:course_detail",
        course_id=enrollment.course.id,
    )