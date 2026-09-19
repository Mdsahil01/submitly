from django import forms

from .models import Assignment


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            "title",
            "description",
            "due_date",
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
            "due_date": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                }
            ),
        }