from django.contrib import admin

from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        "student",
        "assignment",
        "submitted_at",
        "status",
    )

    list_filter = (
        "status",
        "submitted_at",
    )

    search_fields = (
        "student__full_name",
        "student__email",
        "assignment__title",
    )

    ordering = ("-submitted_at",)