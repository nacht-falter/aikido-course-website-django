from django import forms

from courses.models import CourseSession

from .models import GuestCourseRegistration, UserCourseRegistration


class UserCourseRegistrationForm(forms.ModelForm):
    # Pass course instance to form (adapted from:
    # https://medium.com/analytics-vidhya/django-how-to-pass-the-
    # user-object-into-form-classes-ee322f02948c):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)
        user_profile = kwargs.pop("user_profile", None)
        super().__init__(*args, **kwargs)

        if course:
            self.fields["selected_sessions"].queryset = CourseSession.objects.filter(
                course=course).order_by("date", "start_time")

            if course.course_type == "international":
                self.fields['dinner'] = forms.BooleanField(
                    required=False, label="I would like to join the dinner")
                self.fields['overnight_stay'] = forms.BooleanField(
                    required=False, label="I need a place to stay overnight")

        if user_profile.grade >= 6:
            self.fields["exam"].widget = forms.HiddenInput()

    accept_terms = forms.BooleanField(
        required=True, label="I accept the terms and conditions"
    )
    selected_sessions = forms.ModelMultipleChoiceField(
        label="I will attend the following sessions:",
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    exam = forms.BooleanField(
        required=False, label="I want to apply for an exam")

    discount = forms.BooleanField(
        required=False, label="I am eligible for a discount")

    class Meta:
        model = UserCourseRegistration
        fields = [
            "selected_sessions",
            "exam",
            "payment_method",
            "discount",
            "comment",
            "accept_terms",
        ]


class GuestCourseRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)
        super().__init__(*args, **kwargs)
        if course:
            self.fields["selected_sessions"].queryset = CourseSession.objects.filter(
                course=course)

            if course.course_type == "international":
                self.fields['dinner'] = forms.BooleanField(
                    required=False, label="I would like to join the dinner")
                self.fields['overnight_stay'] = forms.BooleanField(
                    required=False, label="I need a place to stay overnight")

    accept_terms = forms.BooleanField(
        required=True, label="I accept the terms and conditions"
    )
    selected_sessions = forms.ModelMultipleChoiceField(
        label="I will attend the following sessions:",
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    exam = forms.BooleanField(
        required=False, label="I want to apply for an exam")

    discount = forms.BooleanField(
        required=False, label="I am eligible for a discount")

    other_dojo = forms.CharField(required=True, initial="Other Dojo")

    class Meta:
        model = GuestCourseRegistration
        fields = [
            "email",
            "first_name",
            "last_name",
            "selected_sessions",
            "dojo",
            "other_dojo",
            "grade",
            "exam",
            "payment_method",
            "discount",
            "comment",
            "accept_terms",
        ]
