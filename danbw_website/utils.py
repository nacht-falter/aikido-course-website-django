import os

from django.conf import settings
from django.core.mail import send_mail


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
    registration,
    course,
    sessions,
    is_authenticated=False
):
    """Sends a registration confirmation email"""

    subject = f"[Dynamic Aikido Nocquet BW] You signed up for {registration.course}"
    message_parts = [
        f"Hi {registration.user.first_name if is_authenticated else registration.first_name},\n",
        "You have successfully signed up ",
        f"for {course}\n",
        f"\nCourse dates: {course.start_date.strftime('%b %d')} to ",
        f"{course.end_date.strftime('%b %d, %Y')}\n",
        "\nRegistration details:\n",
        "- Selected sessions: \n    ",
        "\n    ".join(sessions),
        "\n",
        f"- Fee: {registration.final_fee} €\n",
        f"- Payment method: {registration.get_payment_method_display()}\n",
    ]

    if registration.exam:
        message_parts += [
            f"- You applied for an exam for {registration.get_exam_grade_display()}\n"
        ]

    if registration.payment_method == 0:
        message_parts += [
            "\n\nPlease transfer the fee to the following account until ",
            f"{course.bank_transfer_until.strftime('%b %d, %Y')}:\n",
            f"{os.environ.get('BANK_ACCOUNT')}\n",
        ]

    sender = settings.EMAIL_HOST_USER
    recipient = registration.user.email if is_authenticated else registration.email
    message = "".join(message_parts)
    send_mail(subject, message, sender, [recipient])


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
