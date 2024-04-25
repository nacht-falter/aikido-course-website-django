from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import User

from allauth.account.signals import email_confirmed

# Instructions for using signals:
# Instructionshttps://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/

# Documentation for django allauth signals:
# https://django-allauth.readthedocs.io/en/latest/signals.html


@receiver(email_confirmed)
def email_confirmed(request, email_address, **kwargs):
    user = User.objects.get(email=email_address)

    send_mail(
        "[DANBW e.V.] Email confirmation successful",
        (
            f"Hi, {user},\n"
            "you have successfully confirmed your email address.\n"
            "You can login to your account at: "
            f"{request.META['HTTP_HOST']}/accounts/login"
        ),
        settings.EMAIL_HOST_USER,
        [email_address],
    )
