from allauth.account.forms import SignupForm
from captcha.fields import CaptchaField 


class CustomSignupForm(SignupForm):
    captcha = CaptchaField()

    field_order = ['username', 'email', 'password1', 'password2', 'captcha']

    def save(self, request):

        user = super(CustomSignupForm, self).save(request)

        return user
