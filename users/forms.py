from django import forms
from django.utils.translation import gettext as _

from danbw_website import constants, utils

from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    # Add new fields to form: https://stackoverflow.com/a/58944671
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": _("First Name")}),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": _("Last Name")}),
    )
    dojo = forms.ChoiceField(
        required=True,
        choices=constants.DOJO_CHOICES,
    )
    other_dojo = forms.CharField(
        required=False,
        label=_("Other Dojo"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter the name of your Dojo")}),
    )

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "grade",
            "dojo",
            "other_dojo",
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


class UpdateUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": _("First Name")}),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": _("Last Name")}),
    )
    dojo = forms.ChoiceField(
        required=True,
        choices=constants.DOJO_CHOICES,
    )
    other_dojo = forms.CharField(
        required=False,
        label=_("Other Dojo"),
        widget=forms.TextInput(
            attrs={"placeholder": _("Enter the name of your Dojo")}),
    )

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "grade",
            "dojo",
            "other_dojo",
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
