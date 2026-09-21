from django.urls import path

from . import views

app_name = "submissions"

urlpatterns = [
    path(
        "<int:assignment_id>/create/",
        views.create_submission,
        name="create_submission",
    ),
    path(
        "<int:submission_id>/",
        views.submission_detail,
        name="submission_detail",
    ),
]
