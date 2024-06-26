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
        _("Hi,\n"),
        _("you have successfully confirmed your email address {email}.\n").format(
            email=user.email),
        _("You can login to your account at: {login_url}").format(
            login_url=f"{request.META['HTTP_HOST']}/accounts/login")
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


def write_registrations_csv(writer, registrations):
    """Write registration data to CSV"""

    header_row = [
        "First Name",
        "Last Name",
        "Email",
        "Grade",
        "Selected Sessions",
        "Exam",
        "Exam Grade",
        "Accept Terms",
        "Final Fee",
        "Payment Status"
    ]
    if registrations and registrations[0].course.course_type == "international":
        header_row.append("Dinner")
        header_row.append("Overnight Stay")
    writer.writerow(header_row)

    for registration in registrations:
        selected_sessions = ", ".join(
            session.title for session in registration.selected_sessions.all())

        if hasattr(registration, "user"):
            user = registration.user
        else:
            user = None

        data_row = [
            user.first_name if user else registration.first_name,
            user.last_name if user else registration.last_name,
            user.email if user else registration.email,
            user.profile.get_grade_display() if user else registration.get_grade_display(),
            selected_sessions,
            "Yes" if registration.exam else "No",
            registration.get_exam_grade_display(),
            "Yes" if registration.accept_terms else "No",
            registration.final_fee,
            registration.get_payment_status_display(),
        ]
        if registration.course.course_type == "international":
            data_row.append("Yes" if registration.dinner else "No")
            data_row.append("Yes" if registration.overnight_stay else "No")
        writer.writerow(data_row)
