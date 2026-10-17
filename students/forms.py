
from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ["full_name", "email", "phone", "course"]

    def clean_email(self):
        email = self.cleaned_data["email"].strip()

        if Student.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "A student with this email already exists."
            )

        return email
