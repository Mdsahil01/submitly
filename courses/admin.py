from django.contrib import admin
from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'faculty', 'created_at')
    list_filter = ('faculty', 'created_at')
    search_fields = ('code', 'name', 'faculty__full_name', 'faculty__email')
    ordering = ('code',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')
    list_filter = ('course', 'enrolled_at')
    search_fields = ('student__full_name', 'student__email', 'course__code', 'course__name')
    ordering = ('-enrolled_at',)
