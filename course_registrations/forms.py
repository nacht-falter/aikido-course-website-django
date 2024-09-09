from django import forms
from django.utils.translation import gettext_lazy as _

from courses.models import CourseSession
from danbw_website import constants, utils

from .models import CourseRegistration


class CourseRegistrationForm(forms.ModelForm):
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
                    required=False, label=_("I would like to join the dinner"))
                self.fields['overnight_stay'] = forms.BooleanField(
                    required=False, label=_("I need a place to stay overnight"))

        if user_profile:
            if user_profile.grade >= 6:
                self.fields["exam"].widget = forms.HiddenInput()

            self.fields["email"].widget = forms.HiddenInput()
            self.fields["first_name"].widget = forms.HiddenInput()
            self.fields["last_name"].widget = forms.HiddenInput()
            self.fields["dojo"].widget = forms.HiddenInput()
            self.fields["grade"].widget = forms.HiddenInput()
            self.fields["other_dojo"].widget = forms.HiddenInput()
        else:
            self.fields["email"].required = True
            self.fields["first_name"].required = True
            self.fields["last_name"].required = True
            self.fields["dojo"].required = True
            self.fields["grade"].required = True
            self.fields["other_dojo"].initial = _("Other Dojo")

    accept_terms = forms.BooleanField(
        required=True, label=_("I accept the terms and conditions")
    )
    selected_sessions = forms.ModelMultipleChoiceField(
        label=_("I will attend the following sessions:"),
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    exam = forms.BooleanField(
        required=False, label=_("I want to apply for an exam")
    )
    discount = forms.BooleanField(
        required=False, label=_("I am eligible for a discount")
    )
    dojo = forms.ChoiceField(
        required=False,
        choices=constants.DOJO_CHOICES,
    )
    other_dojo = forms.CharField(
        required=False,
        label=_("Other Dojo"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter the name of your Dojo")}),
    )

    class Meta:
        model = CourseRegistration
        fields = [
            "email",
            "first_name",
            "last_name",
            "selected_sessions",
            "dojo",
            "grade",
            "exam",
            "payment_method",
            "discount",
            "comment",
            "accept_terms",
            "dinner",
            "overnight_stay",
        ]

    def clean(self):
        cleaned_data = super().clean()
        dojo = cleaned_data.get("dojo")
        other_dojo = cleaned_data.get("other_dojo")
        if dojo == "other":
            if not other_dojo:
                self.add_error("other_dojo", _(
                    "Please specify a dojo if you select 'Other'."))
            cleaned_data["dojo"] = other_dojo
        else:
            dojo_display_value = utils.get_tuple_value(
                constants.DOJO_CHOICES, dojo)
            cleaned_data["dojo"] = dojo_display_value

        return cleaned_data
