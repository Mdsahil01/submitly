from django import forms

from .models import Submission


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["content", "file"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 12,
                    "placeholder": "Write your answer here...",
                }
            ),
        }

    def clean_file(self):
        file = self.cleaned_data.get("file")
        if not file:
            return None
        
        # Additional validation at form level
        allowed_extensions = [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".txt"]
        ext = file.name.split(".")[-1].lower()
        if f".{ext}" not in allowed_extensions:
            raise forms.ValidationError(
                f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        return file
