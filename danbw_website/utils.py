import os
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation
from django.utils.formats import date_format, time_format
from django.utils.translation import gettext as _

from danbw_website import constants


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
    try:
        send_mail(subject, message, sender, [recipient])
    except SMTPException:
        messages.error(request, _(
            "Failed to send email confirmation email. Please contact the course team."))


def send_registration_confirmation(request, registration):
    """Sends a registration confirmation email"""

    translation.activate(request.LANGUAGE_CODE)

    sessions = [
        f"{date_format(session.date)}, "
        f"{time_format(session.start_time)} to "
        f"{time_format(session.end_time)}: "
        f"{session.title}"
        for session in registration.selected_sessions.all()
    ]

    translation.deactivate()

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

    try:
        send_mail(subject, message, sender, [recipient], html_message=message)
    except SMTPException as e:
        raise SMTPException(
            _("Invalid email address. Please try again with a valid email address.")) from e


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
    try:
        send_mail(subject, message, sender, [recipient])
    except SMTPException as e:
        raise SMTPException(
            _("Failed to send registration notification email. Please contact the course team.")) from e


def send_membership_confirmation(first_name, email, membership_type):
    """Sends a membership confirmation email"""
    membership = get_tuple_value(constants.MEMBERSHIP_TYPES, membership_type)
    subject = _("[Dynamic Aikido Nocquet BW] Your {membership} application").format(
        membership=membership)
    bank_details = os.environ.get("BANK_ACCOUNT")

    if membership_type == "dan_international" or membership_type == "danbw":
        payment_information = _(
            "The membership fee for the current year will be deducted from your account.\n")
    else:
        fee = get_tuple_value(constants.MEMBERSHIP_FEES, membership_type)
        payment_information = _(
            f"Please transfer the fee of €{fee} to the account below:\n\n")

    message_parts = [
        _("Hi {first_name},\n\n").format(first_name=first_name),
        _("We have received your {membership} application.\n\n").format(
            membership=membership),
        payment_information,
        f"{bank_details}\n\n" if membership_type == 'childrens_passport' else "",
        _("In the meantime, we will issue your passport."),
        _("You don't need to do anything else for now.\n\n"),
        _("Best regards,\n"),
        _("The D.A.N. BW team\n"),
    ]

    sender = settings.EMAIL_HOST_USER
    recipient = email
    message = "".join(message_parts)

    try:
        send_mail(subject, message, sender, [recipient])
    except SMTPException as e:
        raise SMTPException(
            _("Invalid email address. Please try again with a valid email address.")) from e


def send_membership_notification(first_name, last_name, email, dojo, membership_type):
    """Sends a membership notification email"""
    membership = get_tuple_value(constants.MEMBERSHIP_TYPES, membership_type)
    subject = _("[Dynamic Aikido Nocquet BW] New {membership} application").format(
        membership=membership)
    message_parts = [
        _("Hi,\n\n"),
        _("A new {membership} application has been received.\n\n").format(
            membership=membership),
        _("Name: {first_name} {last_name}\n").format(
            first_name=first_name, last_name=last_name),
        _("Email: {email}\n").format(email=email),
        _("Dojo: {dojo}\n\n").format(dojo=dojo),
        _("Please check the admin panel at {site_url}/admin for more details.\n\n").format(
            site_url=os.environ.get("SITE_URL")),
    ]
    sender = settings.EMAIL_HOST_USER
    recipient = os.environ.get("TREASURER_EMAIL")
    message = "".join(message_parts)
    try:
        send_mail(subject, message, sender, [recipient])
    except SMTPException as e:
        raise SMTPException(
            _("Failed to send membership notification email. Please contact the course team.")) from e


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

def get_tuple_value(tuple_of_tuples, key):
    for k, v in tuple_of_tuples:
        if k == key:
            return v
    return None
