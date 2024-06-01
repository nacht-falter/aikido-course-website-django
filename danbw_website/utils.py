import os

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.formats import date_format, time_format


def send_email_confirmation(user, request):
    subject = "[Dynamic Aikido Nocquet BW] Email confirmation successful"
    message_parts = [
        "Hi,\n",
        f"you have successfully confirmed your email address {user.email}.\n",
        "You can login to your account at: ",
        f"{request.META['HTTP_HOST']}/accounts/login",
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

    subject = f"[Dynamic Aikido Nocquet BW] You signed up for {registration.course}"
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
    subject = "[Dynamic Aikido Nocquet BW] Your membership application"
    message_parts = [
        f"Hi {first_name},\n\n",
        "We have received your membership application.\n",
        "The membership fee for the current year will be deducted from your account.\n\n"
        "In the meantime, we will issue your passport. You don't need to do anything else for now.\n\n",
        "Best regards,\n"
        "The DANBW team\n"
    ]
    sender = settings.EMAIL_HOST_USER
    recipient = email
    message = "".join(message_parts)
    send_mail(subject, message, sender, [recipient])
