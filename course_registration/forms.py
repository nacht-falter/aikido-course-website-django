from django import forms

from .models import (CourseSession, GuestCourseRegistration,
                    UserCourseRegistration, UserProfile, GRADE_CHOICES)


class UserCourseRegistrationForm(forms.ModelForm):
    # Pass course instance to form (adapted from:
    # https://medium.com/analytics-vidhya/django-how-to-pass-the-
    # user-object-into-form-classes-ee322f02948c):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)
        user_profile = kwargs.pop("user_profile", None)
        super().__init__(*args, **kwargs)
        self.fields[
            "selected_sessions"
        ].queryset = CourseSession.objects.filter(course=course)
        if user_profile.grade >= 6:
            self.fields["exam"].widget = forms.HiddenInput()

    accept_terms = forms.BooleanField(required=True)
    selected_sessions = forms.ModelMultipleChoiceField(
        label="Select sessions:",
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    class Meta:
        model = UserCourseRegistration
        fields = [
            "selected_sessions",
            "exam",
            "accept_terms",
            "comment",
        ]


class GuestCourseRegistrationForm(forms.ModelForm):
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
    grade = forms.ChoiceField(
        choices=GRADE_CHOICES, required=True
    )

    class Meta:
        model = GuestCourseRegistration
        fields = [
            "email",
            "first_name",
            "last_name",
            "selected_sessions",
            "grade",
            "exam",
            "accept_terms",
            "comment",
        ]


class UserProfileForm(forms.ModelForm):
    # Add new fields to form: https://stackoverflow.com/a/58944671
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "First Name"}),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Last Name"}),
    )

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "grade",
        ]


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


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label="Your email")
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
