from django import forms
from django.utils.translation import gettext_lazy as _
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True, label=_("Your email"))
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()

    # This is a fake honeypot field:
    website = forms.CharField(required=True, label=_("Your website"), max_length=100)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        # Remove the required attribute from the website field on form submission
        if self.is_bound:
            self.fields['website'].required = False
