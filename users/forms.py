from django import forms

from .models import UserProfile


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
            "dojo",
        ]


class UpdateUserProfileForm(forms.ModelForm):
    # Add new fields to form: https://stackoverflow.com/a/58944671
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "grade",
            "dojo"
        ]
