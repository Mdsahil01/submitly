from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Course(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name="Course Name"
    )
    code = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Course Code"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Description"
    )
    faculty = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='courses',
        limit_choices_to={'role': 'FACULTY'},
        verbose_name="Faculty Owner"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Created At"
    )

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.name}"

    def clean(self):
        super().clean()
        if self.faculty_id and not self.faculty.is_faculty:
            raise ValidationError({'faculty': "Course owner must have a FACULTY role."})


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='enrollments',
        limit_choices_to={'role': 'STUDENT'},
        verbose_name="Student"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name="Course"
    )
    enrolled_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Enrolled At"
    )

    class Meta:
        verbose_name = "Enrollment"
        verbose_name_plural = "Enrollments"
        ordering = ['-enrolled_at']
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course_enrollment'
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} enrolled in {self.course.code}"

    def clean(self):
        super().clean()
        if self.student_id and not self.student.is_student:
            raise ValidationError({'student': "Enrolled user must have a STUDENT role."})
