import os
from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
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

    sender = settings.DEFAULT_FROM_EMAIL
    recipient = registration.user.email if request.user.is_authenticated else registration.email

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=sender,
            to=[recipient],
        )
        email.content_subtype = 'html'
        email.send()
    except SMTPException as e:
        raise SMTPException(
            _("Invalid email address. Please try again with a valid email address.")
        ) from e


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

    if membership_type == "dan_international":
        payment_information = _(
            "The membership fees will be deducted from your account.\n")
    else:
        fee = get_tuple_value(constants.MEMBERSHIP_FEES, membership_type)
        if membership_type == 'danbw':
            payment_information = _(
                "Please transfer the annual fee of €{fee} to the account below:\n\n").format(fee=fee)
        else:
            payment_information = _(
                "Please transfer the fee of €{fee} to the account below:\n\n").format(fee=fee)

    if membership_type == "danbw":
        passport = ""
    else:
        passport = _("We will issue your passport as soon as possible.\n\n"
                     "You don't need to do anything else for now.\n\n")

    message_parts = [
        _("Hi {first_name},\n\n").format(first_name=first_name),
        _("We have received your {membership} application.\n\n").format(
            membership=membership),
        payment_information,
        f"{bank_details}\n\n" if membership_type != 'dan_international' else "",
        f"{passport}\n" if membership_type != 'danbw' else "",
        _("Best regards,\n"),
        _("The D.A.N. BW team\n"),
    ]

    sender = os.environ.get("CONTACT_EMAIL")
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
        _("Course"),
        _("First Name"),
        _("Last Name"),
        _("Email"),
        _("Grade"),
        _("Dojo"),
        _("Selected Sessions"),
        _("Final Fee"),
        _("Discount"),
        _("Payment Method"),
        _("Payment Status"),
        _("Exam"),
        _("Exam Grade"),
        _("Comment"),
        _("Accept Terms"),
        _("Registration Date"),
    ]
    if registrations and registrations[0].course.has_dinner:
        header_row.append("Dinner")
        header_row.append("Overnight Stay")
    writer.writerow(header_row)

    for registration in registrations:
        selected_sessions = ", ".join(
            f"{session.date.strftime('%d.%m.%Y')}, {session.start_time.strftime('%H:%M')}"
            f"-{session.end_time.strftime('%H:%M')}: {session.title}"
            for session in registration.selected_sessions.all()
        )

        if hasattr(registration, "user"):
            user = registration.user
        else:
            user = None

        data_row = [
            registration.course.title,
            user.first_name if user else registration.first_name,
            user.last_name if user else registration.last_name,
            user.email if user else registration.email,
            user.profile.get_grade_display() if user else registration.get_grade_display(),
            user.profile.dojo if user else registration.dojo,
            selected_sessions,
            registration.final_fee,
            _("Yes") if registration.discount else _("No"),
            registration.get_payment_method_display(),
            registration.get_payment_status_display(),
            _("Yes") if registration.exam else _("No"),
            registration.get_exam_grade_display(),
            registration.comment,
            _("Yes") if registration.accept_terms else _("No"),
            registration.registration_date.strftime("%d.%m.%Y, %H:%M:%S"),
        ]
        if registration.course.has_dinner:
            data_row.append(_("Yes") if registration.dinner else _("No"))
            data_row.append(
                _("Yes") if registration.overnight_stay else _("No"))
        writer.writerow(data_row)


def write_membership_csv(writer, memberships):
    """Write membership data to CSV"""

    header_row = [
        _("First Name"),
        _("Last Name"),
        _("Date of Birth"),
        _("Email"),
        _("Street"),
        _("Street Number"),
        _("Postcode"),
        _("City"),
        _("Phone Home"),
        _("Phone Mobile"),
        _("Grade"),
        _("Dojo"),
        _("Accept Terms"),
    ]
    writer.writerow(header_row)

    for membership in memberships:
        if hasattr(membership, "user"):
            user = membership.user
        else:
            user = None

        data_row = [
            user.first_name if user else membership.first_name,
            user.last_name if user else membership.last_name,
            membership.date_of_birth,
            user.email if user else membership.email,
            membership.street,
            membership.street_number,
            membership.postcode,
            membership.city,
            membership.phone_home,
            membership.phone_mobile,
            user.profile.get_grade_display() if user else membership.get_grade_display(),
            user.profile.dojo if user else membership.dojo,
            _("Yes") if membership.accept_terms else _("No"),
        ]
        writer.writerow(data_row)


def get_tuple_value(tuple_of_tuples, key):
    for k, v in tuple_of_tuples:
        if k == key:
            return v
    return None


def get_tuple_key(tuple_of_tuples, value):
    for k, v in tuple_of_tuples:
        if v == value:
            return k
    return None
