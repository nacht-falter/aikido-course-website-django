from django import forms
from django.utils.translation import gettext as _

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
    other_dojo = forms.CharField(
        required=True,
        label=_("Other Dojo"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter the name of your Dojo")}),
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


class UpdateUserProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": _("First Name")}),
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": _("Last Name")}),
    )
    other_dojo = forms.CharField(
        required=True,
        label=_("Other Dojo"),
        widget=forms.TextInput(attrs={"placeholder": _("Enter the name of your Dojo")}),
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
