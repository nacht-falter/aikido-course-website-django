import os

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.formats import date_format, time_format
from django.utils.translation import gettext as _


def send_email_confirmation(user, request):
    subject = _("[Dynamic Aikido Nocquet BW] Email confirmation successful")
    message_parts = [
        _(
            "Hi,\n",
            f"you have successfully confirmed your email address {user.email}.\n",
            "You can login to your account at: ",
            f"{request.META['HTTP_HOST']}/accounts/login",
        )
    ]
    sender = settings.EMAIL_HOST_USER
    recipient = user.email
    message = "".join(message_parts)
    send_mail(subject, message, sender, [recipient])


def send_registration_confirmation(
    request,
    registration,
):
    """Sends a registration confirmation email"""

    translation.activate(request.LANGUAGE_CODE)

    sessions = [
        f"{date_format(session.date)}, "
        f"{time_format(session.start_time)} to "
        f"{time_format(session.end_time)}: "
        f"{session.title}"
        for session in registration.selected_sessions.all()
    ]

    subject = _("[Dynamic Aikido Nocquet BW] You signed up for ") + \
        registration.course.title
    context = {
        'request': request,
        'registration': registration,
        'sessions': sessions,
        'subject': subject,
        'bank_account': os.environ.get('BANK_ACCOUNT'),
    }

    message = render_to_string('registration_confirmation.html', context)

    sender = settings.EMAIL_HOST_USER
    recipient = registration.user.email if request.user.is_authenticated else registration.email
    send_mail(subject, message, sender, [recipient], html_message=message)

    translation.deactivate()


def send_membership_confirmation(first_name, email):
    """Sends a membership confirmation email"""
    subject = _("[Dynamic Aikido Nocquet BW] Your membership application")
    message_parts = [
        _("Hi {first_name},\n").format(first_name=first_name),
        _("We have received your membership application.\n"),
        _("The membership fee for the current year will be deducted from your account.\n\n"),
        _("In the meantime, we will issue your passport. You don't need to do anything else for now.\n\n"),
        _("Best regards,\n"),
        _("The DANBW team\n"),
    ]
    sender = settings.EMAIL_HOST_USER
    recipient = email
    message = "".join(message_parts)
    send_mail(subject, message, sender, [recipient])
