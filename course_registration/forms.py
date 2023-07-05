from django import forms
from .models import CourseRegistration


class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistration
        fields = [
            "exam",
            "accept_terms",
            "comment",
            "final_fee",
        ]
