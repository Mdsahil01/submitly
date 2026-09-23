from django.urls import path

from . import views


app_name = "courses"

urlpatterns = [
    path(
        "",
        views.course_list,
        name="course_list",
    ),
    path(
        "create/",
        views.create_course,
        name="course_create",
    ),
    path(
        "<int:course_id>/",
        views.course_detail,
        name="course_detail",
    ),
    path(
        "<int:course_id>/enroll/",
        views.enroll_course,
        name="enroll_course",
    ),
    path(
    "enrollment/<int:enrollment_id>/approve/",
    views.approve_enrollment,
    name="approve_enrollment",
),

path(
    "enrollment/<int:enrollment_id>/reject/",
    views.reject_enrollment,
    name="reject_enrollment",
),
]