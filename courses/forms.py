from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "code", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "e.g. Software Engineering"}
            ),
            "code": forms.TextInput(
                attrs={"placeholder": "e.g. SE101"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe the course..."
                }
            ),
        }
