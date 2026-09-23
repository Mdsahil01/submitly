import os

from django import forms

from .models import Assignment


class AssignmentForm(forms.ModelForm):

    due_date = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={
                "type": "datetime-local",
            },
        ),
    )

    class Meta:
        model = Assignment
        fields = [
            "title",
            "description",
            "reference_file",
            "due_date",
            "max_marks",
            "is_published",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter assignment title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Enter assignment instructions",
                    "rows": 6,
                }
            ),
            "max_marks": forms.NumberInput(
                attrs={
                    "placeholder": "Enter maximum marks",
                    "step": "0.01",
                    "min": "0",
                }
            ),
        }

    def clean_reference_file(self):
        file = self.cleaned_data.get("reference_file")

        if not file:
            return file

        allowed_extensions = {
            ".pdf",
            ".doc",
            ".docx",
            ".ppt",
            ".pptx",
            ".txt",
        }

        extension = os.path.splitext(file.name)[1].lower()

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Unsupported file type. Allowed files: PDF, DOC, DOCX, PPT, PPTX, TXT."
            )

        max_size = 10 * 1024 * 1024

        if file.size > max_size:
            raise forms.ValidationError(
                "File size must not exceed 10 MB."
            )

        return file