from django.test import TestCase, RequestFactory
from django.core import mail
from django.contrib.auth.models import User
from .signals import email_confirmed


class SignalTest(TestCase):
    def test_confirmation_success_email(self):
        print("\ntest_confirmation_success_email")
        user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )

        # Create a mock request: https://docs.djangoproject.com/en/4.2/
        # topics/testing/advanced/#the-request-factory
        factory = RequestFactory()
        request = factory.get("/")
        request.META["HTTP_HOST"] = "www.test.com"

        email_confirmed(request=request, email_address=user.email)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "[DANBW e.V.] Email confirmation successful",
        )
