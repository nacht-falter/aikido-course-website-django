from django import forms

from .models import CourseRegistration, UserProfile, CourseSession


class CourseRegistrationForm(forms.ModelForm):
    # Pass course instance to form (adapted from:
    # https://medium.com/analytics-vidhya/django-how-to-pass-the-
    # user-object-into-form-classes-ee322f02948c):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)
        super().__init__(*args, **kwargs)
        self.fields[
            "selected_sessions"
        ].queryset = CourseSession.objects.filter(course=course)

    accept_terms = forms.BooleanField(required=True)
    selected_sessions = forms.ModelMultipleChoiceField(
        label="Select sessions:",
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = CourseRegistration
        fields = [
            "selected_sessions",
            "exam",
            "accept_terms",
            "comment",
        ]


class UserProfileForm(forms.ModelForm):
    # Add new fields to form: https://stackoverflow.com/a/58944671
    first_name = forms.CharField(max_length=200)
    last_name = forms.CharField(max_length=200)

    class Meta:
        model = UserProfile
        fields = ["grade"]


class UpdateUserProfileForm(forms.ModelForm):
    # Add new fields to form: https://stackoverflow.com/a/58944671
    username = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "grade",
        ]
