from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    reference_file = models.FileField(
     upload_to="assignment_references/",
     blank=True,
     null=True,
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="assignments",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_assignments",
        limit_choices_to={"role": "FACULTY"},
    )
    due_date = models.DateTimeField()
    max_marks = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=100.00,
        verbose_name="Maximum Marks"
    )
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
     if self.created_by_id:
         if not self.created_by.is_faculty:
             raise ValidationError(
                {"created_by": "Only Faculty users can create assignments."}
            )

     if self.course_id and self.created_by_id:
         if self.course.faculty_id != self.created_by_id:
             raise ValidationError(
                 {
                     "created_by": (
                        "Faculty can only create assignments "
                        "for their own courses."
                    )
                 }
             )

    def __str__(self):
        return f"{self.course.code} - {self.title}"