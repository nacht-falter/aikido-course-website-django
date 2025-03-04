import random
import time

from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField
from django import forms


class CustomSignupForm(SignupForm):
    captcha = CaptchaField()
    timestamp = forms.FloatField(
        widget=forms.HiddenInput(), required=False)
    phone_number = forms.CharField(
        required=False, widget=forms.HiddenInput())  # Honeypot

    field_order = ["username", "email", "phone_number",
                   "password1", "password2", "captcha"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["timestamp"].initial = time.time()

    def clean(self):
        cleaned_data = super().clean()
        form_timestamp = cleaned_data.get("timestamp", 0)

        if form_timestamp and time.time() - form_timestamp < 15:
            # Add a random delay before failing to deter bots
            time.sleep(random.uniform(2, 4))
            raise forms.ValidationError(
                "Form could not be submitted. Please try again.")

        return cleaned_data

    def clean_phone_number(self):
        value = self.cleaned_data.get("phone_number")
        if value:
            raise forms.ValidationError(
                "Form could not be submitted. Please try again.")
        return value

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user
