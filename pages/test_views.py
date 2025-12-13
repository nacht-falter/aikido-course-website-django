from captcha.models import CaptchaStore
from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from .models import Category, Page


class ContactPageTest(TestCase):
    """Tests for Contact Page view"""

    def _get_captcha(self):
        """Helper method to get a valid captcha for testing"""
        captcha = CaptchaStore.objects.create(challenge='test', response='test')
        return {
            'captcha_0': captcha.hashkey,
            'captcha_1': 'test',
        }

    def test_get_contact_page(self):
        print("\ntest_get_contact_page")
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("contact.html")

    def test_post_valid_contact_form(self):
        print("\ntest_post_valid_contact_form")
        form_data = {
            "subject": "Test Subject",
            "message": "Test message",
            "from_email": "from@example.com",
            **self._get_captcha(),
        }
        response = self.client.post(reverse("contact"), form_data)
        self.assertRedirects(response, reverse("home"), 302, 200)

        # Test email documentation: https://docs.djangoproject.com/en/
        # 4.2/topics/testing/tools/#email-services
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[D.A.N.BW Contact Form]: Test Subject")

    def test_post_invalid_contact_form(self):
        print("\ntest_post_invalid_contact_form")
        response = self.client.post(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_bad_header_error(self):
        print("\ntest_post_invalid_contact_form")

        # Test bad header: https://stackoverflow.com/a/27268861
        form_data = {
            "subject": "Test\nSubject",
            "message": "Test message",
            "from_email": "from@example.com",
            **self._get_captcha(),
        }
        response = self.client.post(reverse("contact"), form_data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Ungültiger Header gefunden. Bitte versuche es erneut.",
            messages,
        )


class PageTest(TestCase):
    """Tests for PageList view"""

    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
        )
        self.page = Page.objects.create(
            title="Test page",
            slug="test-page",
            category=self.category,
            status=1,
            content="Test Content",
        )

    def test_get_page_list(self):
        print("\ntest_get_page_list")
        response = self.client.get(reverse("page_list", kwargs={"category_slug": self.category.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["object_list"], Page.objects.all()
        )

        self.assertEqual(response.status_code, 200)
