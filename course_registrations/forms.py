from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from courses.models import CourseSession
from danbw_website import constants, utils

from .models import CourseRegistration


class CourseRegistrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop("course", None)
        user_profile = kwargs.pop("user_profile", None)
        super().__init__(*args, **kwargs)

        self.course = course
        self.user_profile = user_profile

        if course:
            self.fields["selected_sessions"].queryset = CourseSession.objects.filter(
                course=course
            )

            self.fields['dinner'] = forms.BooleanField(
                required=False, label=_("I would like to join the dinner on Saturday evening."))
            self.fields['overnight_stay'] = forms.BooleanField(
                required=False, label=_("I need a place to stay overnight."))

        if user_profile:
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

        if (
            course.course_type not in constants.EXAM_COURSES or
            course.fee_category == 'dan_seminar'
        ):
            self.fields["exam"].widget = forms.HiddenInput()

        if user_profile and user_profile.grade >= 6:
            self.fields["exam"].disabled = True

    accept_terms = forms.BooleanField(
        required=True, label=_("I accept the terms and conditions below.")
    )
    selected_sessions = forms.ModelMultipleChoiceField(
        label=_("I will attend the following sessions:"),
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )
    exam = forms.BooleanField(
        required=False, label=_("I want to apply for an exam.")
    )
    discount = forms.BooleanField(
        required=False, label=_("I am eligible for a discount.")
    )
    dan_member = forms.BooleanField(
        required=False, label=_("I am a D.A.N. International member.")
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
            "dan_member",
            "comment",
            "accept_terms",
            "dinner",
            "overnight_stay",
        ]

    def clean(self):
        cleaned_data = super().clean()

        grade = cleaned_data.get("grade")
        selected_sessions = cleaned_data.get("selected_sessions")
        dojo = cleaned_data.get("dojo")
        other_dojo = cleaned_data.get("other_dojo")

        user_profile_grade = self.user_profile.grade if self.user_profile else None

        if self.course.fee_category == "dan_seminar":
            if (
                (user_profile_grade is not None and user_profile_grade <= 5) or
                (grade is not None and grade <= 5)
            ):
                raise ValidationError(
                    _("You need to be 1st Kyu or higher to register for this course.")
                )

        if not selected_sessions:
            raise ValidationError(_("Please select at least one session."))

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
