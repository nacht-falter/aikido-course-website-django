from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase

from .models import Category, Page


class ContactPageTest(TestCase):
    """Tests for Contact Page view"""

    def test_get_contact_page(self):
        print("\ntest_get_contact_page")
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("contact.html")

    def test_post_valid_contact_form(self):
        print("\ntest_post_valid_contact_form")
        form_data = {
            "subject": "Test Subject",
            "message": "Test message",
            "from_email": "from@example.com",
        }
        response = self.client.post("/contact/", form_data)
        self.assertRedirects(response, "/", 302, 200)

        # Test email documentation: https://docs.djangoproject.com/en/
        # 4.2/topics/testing/tools/#email-services
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test Subject")

    def test_post_invalid_contact_form(self):
        print("\ntest_post_invalid_contact_form")
        response = self.client.post("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_bad_header_error(self):
        print("\ntest_post_invalid_contact_form")

        # Test bad header: https://stackoverflow.com/a/27268861
        form_data = {
            "subject": "Test\nSubject",
            "message": "Test message",
            "from_email": "from@example.com",
        }
        response = self.client.post("/contact/", form_data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Invalid Header found. Please try again.",
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
        response = self.client.get(f"/pages/{self.category.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["object_list"], Page.objects.all()
        )

        self.assertEqual(response.status_code, 200)
