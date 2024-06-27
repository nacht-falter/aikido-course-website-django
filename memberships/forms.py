from django import forms
from django.utils.translation import gettext_lazy as _

from danbw_website import constants

from .models import DanIntMembership, ChildrensPassport


class DanIntMembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Get first element of each tuple in DOJO_CHOICES
        dojos = {choice[0] for choice in constants.DOJO_CHOICES}

        if request and request.user.is_authenticated:
            self.fields["first_name"].initial = request.user.first_name
            self.fields["last_name"].initial = request.user.last_name
            self.fields["email"].initial = request.user.email
            self.fields["grade"].initial = request.user.profile.grade
            self.fields["dojo"].initial = (
                request.user.profile.dojo
                if request.user.profile.dojo in dojos
                else "other"
            )
            self.fields["other_dojo"].initial = (
                request.user.profile.dojo
                if request.user.profile.dojo not in dojos
                else ""
            )

    sepa = forms.BooleanField(
        required=True,
        label=_(
            "I agree that the membership fee will be collected by SEPA direct debit from my account below."),
    )
    accept_terms = forms.BooleanField(
        required=True,
        label=_(
            "I accept the above terms and conditions regarding cancellation and data processing and apply for "
            "a membership with DAN International."
        ),
    )
    liability_disclaimer = forms.BooleanField(
        required=True,
        label=_(
            "I am aware that Aikido is a potentially dangerous sport and that the above-mentioned organization "
            "and its representatives are not liable for accidents or injuries that occur during the practice of "
            "Aikido, except within the scope of legal regulations in cases of intent or gross negligence."
        ),
    )

    class Meta:
        model = DanIntMembership
        fields = "__all__"
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }


class ChildrensPassportForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        # Get first element of each tuple in DOJO_CHOICES
        dojos = {choice[0] for choice in constants.DOJO_CHOICES}

        if request and request.user.is_authenticated:
            self.fields["first_name"].initial = request.user.first_name
            self.fields["last_name"].initial = request.user.last_name
            self.fields["email"].initial = request.user.email
            self.fields["grade"].initial = request.user.profile.grade
            self.fields["dojo"].initial = (
                request.user.profile.dojo
                if request.user.profile.dojo in dojos
                else "other"
            )
            self.fields["other_dojo"].initial = (
                request.user.profile.dojo
                if request.user.profile.dojo not in dojos
                else ""
            )

    accept_terms = forms.BooleanField(
        required=True,
        label=_(
            "I accept the above terms and conditions regarding the processing of my data and apply for "
            "a Children's Passport."
        ),
    )
    liability_disclaimer = forms.BooleanField(
        required=True,
        label=_(
            "I am aware that Aikido is a potentially dangerous sport and that the above-mentioned organization "
            "and its representatives are not liable for accidents or injuries that occur during the practice of "
            "Aikido, except within the scope of legal regulations in cases of intent or gross negligence."
        ),
    )

    class Meta:
        model = ChildrensPassport
        fields = "__all__"
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'})
        }
