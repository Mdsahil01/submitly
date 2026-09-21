from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect, render

from assignments.models import Assignment

from .forms import CourseForm
from .models import Course


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
            .filter(enrollments__student=request.user)
            .distinct()
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

            return redirect("courses:course_detail", course_id=course.id)
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
        course = get_object_or_404(
            Course,
            id=course_id,
            enrollments__student=request.user,
        )
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
