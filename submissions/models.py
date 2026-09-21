import os

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

def submission_file_path(instance, filename):
    """Generate upload path for submission files."""
    return os.path.join(
        "submissions",
        str(instance.assignment.id),
        str(instance.student.id),
        filename
    )

class Submission(models.Model):

    STATUS_SUBMITTED = "SUBMITTED"
    STATUS_LATE = "LATE"
    STATUS_REVIEWED = "REVIEWED"

    STATUS_CHOICES = [
        (STATUS_SUBMITTED, "Submitted"),
        (STATUS_LATE, "Late"),
        (STATUS_REVIEWED, "Reviewed"),
    ]

    ALLOWED_EXTENSIONS = [
        ".pdf", ".doc", ".docx", ".ppt", ".pptx", ".txt"
    ]

    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        limit_choices_to={"role": "STUDENT"},
    )

    assignment = models.ForeignKey(
        "assignments.Assignment",
        on_delete=models.CASCADE,
        related_name="submissions",
    )

    content = models.TextField(blank=True)

    file = models.FileField(
        upload_to=submission_file_path,
        blank=True,
        null=True,
    )

    file_name = models.CharField(max_length=255, blank=True)

    submitted_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_SUBMITTED,
    )

    # Evaluation fields
    marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Marks Awarded"
    )

    feedback = models.TextField(
        blank=True,
        verbose_name="Faculty Feedback"
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Reviewed At"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "assignment"],
                name="unique_student_assignment_submission",
            )
        ]

    def clean(self):
        if self.student_id and not self.student.is_student:
            raise ValidationError(
                {"student": "Only Student users can create submissions."}
            )

        if self.student_id and self.assignment_id:
            if not self.assignment.is_published:
                raise ValidationError(
                    "Students can only submit to published assignments."
                )

            if self.assignment.course.enrollments.filter(
                student_id=self.student_id
            ).exists() is False:
                raise ValidationError(
                    "Student is not enrolled in this assignment's course."
                )

        # File validation
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                raise ValidationError(
                    {"file": f"File type not allowed. Allowed types: {', '.join(self.ALLOWED_EXTENSIONS)}"}
                )
            if self.file.size > self.MAX_FILE_SIZE:
                raise ValidationError(
                    {"file": f"File size exceeds maximum allowed size of {self.MAX_FILE_SIZE / (1024 * 1024)}MB"}
                )

        # Marks validation
        if self.marks is not None:
            if self.marks < 0:
                raise ValidationError(
                    {"marks": "Marks cannot be negative."}
                )
            if self.assignment_id and self.marks > self.assignment.max_marks:
                raise ValidationError(
                    {"marks": f"Marks cannot exceed maximum marks ({self.assignment.max_marks})."}
                )

    def save(self, *args, **kwargs):
        # Determine if late on save
        if self.assignment_id and self.submitted_at is None:
            if self.assignment.due_date < timezone.now():
                self.status = self.STATUS_LATE
        
        # Store original file name
        if self.file and not self.file_name:
            self.file_name = os.path.basename(self.file.name)
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.full_name} - {self.assignment.title}"
