from allauth.account.signals import email_confirmed
from django.dispatch import receiver

from danbw_website.utils import send_email_confirmation

from .models import User

# Instructions for using signals:
# Instructionshttps://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/

# Documentation for django allauth signals:
# https://django-allauth.readthedocs.io/en/latest/signals.html


@receiver(email_confirmed)
def email_confirmed(request, email_address, **kwargs):
    try:
        user = User.objects.get(email=email_address)
        send_email_confirmation(user, request)
    except User.DoesNotExist:
        return
