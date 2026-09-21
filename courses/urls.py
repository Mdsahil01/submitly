from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    path("", views.course_list, name="course_list"),
    path("create/", views.create_course, name="course_create"),
    path("<int:course_id>/", views.course_detail, name="course_detail"),
]
