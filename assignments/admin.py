from django.contrib import admin

from .models import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "course",
        "created_by",
        "due_date",
        "is_published",
        "created_at",
    )

    list_filter = (
        "course",
        "is_published",
        "due_date",
    )

    search_fields = (
        "title",
        "description",
        "course__name",
        "course__code",
        "created_by__full_name",
        "created_by__email",
    )

    ordering = ("-created_at",)