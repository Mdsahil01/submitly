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


class EvaluationForm(forms.ModelForm):
    """Form for faculty to evaluate student submissions."""
    
    class Meta:
        model = Submission
        fields = ["marks", "feedback"]
        widgets = {
            "marks": forms.NumberInput(
                attrs={
                    "placeholder": "Enter marks",
                    "step": "0.01",
                    "min": "0",
                }
            ),
            "feedback": forms.Textarea(
                attrs={
                    "rows": 8,
                    "placeholder": "Provide feedback to the student...",
                }
            ),
        }
    
    def __init__(self, *args, **kwargs):
        self.assignment = kwargs.pop('assignment', None)
        super().__init__(*args, **kwargs)
        
        if self.assignment:
            self.fields['marks'].widget.attrs['max'] = str(self.assignment.max_marks)
            self.fields['marks'].help_text = f"Maximum marks: {self.assignment.max_marks}"
    
    def clean_marks(self):
        marks = self.cleaned_data.get('marks')
        if marks is not None:
            if marks < 0:
                raise forms.ValidationError("Marks cannot be negative.")
            if self.assignment and marks > self.assignment.max_marks:
                raise forms.ValidationError(
                    f"Marks cannot exceed maximum marks ({self.assignment.max_marks})."
                )
        return marks
