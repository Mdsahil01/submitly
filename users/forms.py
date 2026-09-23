from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


User = get_user_model()


class StudentRegistrationForm(UserCreationForm):

    full_name = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter your full name",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Enter your email address",
            }
        ),
    )

    class Meta:
        model = User
        fields = [
            "full_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "An account with this email already exists."
            )

        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.full_name = self.cleaned_data["full_name"]
        user.email = self.cleaned_data["email"]
        user.role = "STUDENT"

        if commit:
            user.save()

        return user