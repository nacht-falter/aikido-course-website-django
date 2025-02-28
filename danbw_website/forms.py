from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField
from django import forms


class CustomSignupForm(SignupForm):
    captcha = CaptchaField()

    phone_number = forms.CharField(required=False, widget=forms.HiddenInput()) # Honeypot

    field_order = ['username', 'email', 'phone_number',
                   'password1', 'password2', 'captcha']

    def clean_phone_number(self):
        value = self.cleaned_data.get('phone_number')
        if value:
            raise forms.ValidationError("Bot detected!")
        return value

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        return user
