from django.conf import settings
from django.core.mail import send_mail


def send_registration_confirmation(
    registration,
    course,
    sessions,
    exam,
    is_authenticated=False
):
    """Sends a registration confirmation email"""

    subject = f"[DANBW e.V.] You signed up for {registration.course}"
    message_parts = [
        f"Hi {registration.user},\n" if is_authenticated else f"Hi {registration.first_name},\n",
        "You have successfully signed up ",
        f"for {course}\n",
        f"\nCourse dates: {course.start_date.strftime('%b %d')} to ",
        f"{course.end_date.strftime('%b %d, %Y')}\n",
        "\nRegistration details:\n",
        "- Selected sessions: ",
        f"{(', '.join(sessions))}\n",
        f"- Exam: {exam}\n",
        f"- Fee: {registration.final_fee} €",
    ]

    sender = settings.EMAIL_HOST_USER
    recipient = registration.user.email if is_authenticated else registration.email

    message = ''.join(message_parts)

    send_mail(subject, message, sender, [recipient])
