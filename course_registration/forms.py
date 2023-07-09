from django import forms
from .models import CourseRegistration, UserProfile


class CourseRegistrationForm(forms.ModelForm):
    class Meta:
        model = CourseRegistration
        fields = [
            "exam",
            "accept_terms",
            "comment",
            "final_fee",
        ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["first_name", "last_name", "grade"]
