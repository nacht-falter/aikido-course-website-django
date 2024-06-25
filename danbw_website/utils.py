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

    subject = _("[Dynamic Aikido Nocquet BW] Your Registration for ") + \
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


def send_registration_notification(request, registration):
    """Sends a registration notification email"""
    subject = _("[Dynamic Aikido Nocquet BW] New registration for ") + \
        registration.course.title
    first_name = registration.user.first_name if request.user.is_authenticated else registration.first_name
    last_name = registration.user.last_name if request.user.is_authenticated else registration.last_name
    email = registration.user.email if request.user.is_authenticated else registration.email
    message_parts = [
        _("Hi,\n\n"),
        _("A new registration for {course} has been received.\n\n").format(
            course=registration.course.title),
        _("Name: {first_name} {last_name}\n").format(
            first_name=first_name, last_name=last_name),
        _("Email: {email}\n").format(email=email),
        _("Course: {course}\n\n").format(course=registration.course.title),
        _("Please check the admin panel at {site_url}/admin for more details.\n\n").format(
            site_url=os.environ.get("SITE_URL")),
    ]
    sender = settings.EMAIL_HOST_USER
    recipient = os.environ.get("COURSE_TEAM_EMAIL")
    message = "".join(message_parts)
    send_mail(subject, message, sender, [recipient])


def send_membership_confirmation(first_name, email, membership_type):
    """Sends a membership confirmation email"""
    subject = _("[Dynamic Aikido Nocquet BW] Your {membership_type} membership application").format(
        membership_type=membership_type)
    message_parts = [
        _("Hi {first_name},\n\n").format(first_name=first_name),
        _("We have received your {membership_type} membership application.\n\n").format(
            membership_type=membership_type),
        _("The membership fee for the current year will be deducted from your account.\n"),
        _("In the meantime, we will issue your passport."),
        _("You don't need to do anything else for now.\n\n"),
        _("Best regards,\n"),
        _("The DANBW team\n"),
    ]
    sender = settings.EMAIL_HOST_USER
    recipient = email
    message = "".join(message_parts)
    send_mail(subject, message, sender, [recipient])


def send_membership_notification(first_name, last_name, email, membership_type):
    """Sends a membership notification email"""
    subject = _("[Dynamic Aikido Nocquet BW] New {membership_type} membership application").format(
        membership_type=membership_type)
    message_parts = [
        _("Hi,\n\n"),
        _("A new {membership_type} membership application has been received.\n\n").format(
            membership_type=membership_type),
        _("Name: {first_name} {last_name}\n").format(
            first_name=first_name, last_name=last_name),
        _("Email: {email}\n\n").format(email=email),
        _("Please check the admin panel at {site_url}/admin for more details.\n\n").format(
            site_url=os.environ.get("SITE_URL")),
    ]
    sender = settings.EMAIL_HOST_USER
    recipient = os.environ.get("TREASURER_EMAIL")
    message = "".join(message_parts)
    send_mail(subject, message, sender, [recipient])
