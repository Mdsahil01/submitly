from django.urls import path

from . import views


app_name = "assignments"

urlpatterns = [
    path(
        "courses/<int:course_id>/create/",
        views.create_assignment,
        name="create_assignment",
    ),
    path(
        "student/",
        views.student_assignments,
        name="student_assignments",
    ),
]