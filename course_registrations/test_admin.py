import os
from datetime import date, timedelta
from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from courses.models import InternalCourse
from users.models import User, UserProfile

from .models import CourseRegistration


@patch.dict(os.environ, {"COURSE_TEAM_EMAIL": "team@example.com"})
class EmailParticipantsActionTest(TestCase):
    """Tests for the email_participants admin action"""

    def setUp(self):
        self.url = reverse("admin:course_registrations_courseregistration_changelist")
        self.staff = User.objects.create_superuser(
            username="staff", password="testpassword", email="staff@example.com"
        )
        self.client.force_login(self.staff)
        course = InternalCourse.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="sensei_emmerson",
            fee_category="regular",
        )
        member = User.objects.create_user(
            username="member", password="testpassword", email="member@example.com",
            first_name="Member", last_name="User",
        )
        UserProfile.objects.create(user=member, dojo="AAR", grade=1)
        self.registrations = [
            CourseRegistration.objects.create(
                course=course, user=member, first_name="Member", last_name="User",
                email="old@example.com", accept_terms=True,
            ),
            CourseRegistration.objects.create(
                course=course, first_name="Guest", last_name="One",
                email="guest@example.com", accept_terms=True,
            ),
            # Same address in different case: should only get one email
            CourseRegistration.objects.create(
                course=course, first_name="Guest", last_name="Two",
                email="GUEST@example.com", accept_terms=True,
            ),
            CourseRegistration.objects.create(
                course=course, first_name="No", last_name="Email", accept_terms=True,
            ),
        ]

    def post(self, **data):
        return self.client.post(self.url, {
            "action": "email_participants",
            "_selected_action": [r.pk for r in self.registrations],
            **data,
        })

    def test_compose_page_lists_recipients(self):
        print("\ntest_compose_page_lists_recipients")
        response = self.post()
        self.assertTemplateUsed(response, "admin/course_registrations/email_participants.html")
        self.assertNotContains(response, "old@example.com")
        self.assertEqual(
            sorted(email.lower() for _name, email in response.context["recipients"]),
            ["guest@example.com", "member@example.com"],
        )
        self.assertEqual(len(response.context["missing"]), 1)
        self.assertEqual(len(mail.outbox), 0)

    def test_review_does_not_send(self):
        print("\ntest_review_does_not_send")
        response = self.post(stage="review", subject="Change", message="New time")
        self.assertTrue(response.context["review"])
        self.assertContains(response, "New time")
        self.assertEqual(len(mail.outbox), 0)

    def test_review_with_missing_message_stays_on_compose(self):
        print("\ntest_review_with_missing_message_stays_on_compose")
        response = self.post(stage="review", subject="Change", message="")
        self.assertFalse(response.context["review"])
        self.assertTrue(response.context["form"].errors)

    def test_send_emails_each_participant_and_copies_team(self):
        print("\ntest_send_emails_each_participant_and_copies_team")
        response = self.post(stage="send", subject="Change", message="New time")
        self.assertRedirects(response, self.url, fetch_redirect_response=False)

        participant_mails = [m for m in mail.outbox if m.to != ["team@example.com"]]
        self.assertEqual(
            sorted(m.to[0].lower() for m in participant_mails),
            ["guest@example.com", "member@example.com"],
        )
        for message in participant_mails:
            self.assertEqual(message.subject, "Change")
            self.assertEqual(message.body, "New time")
            self.assertEqual(message.reply_to, ["team@example.com"])

        team_copy = [m for m in mail.outbox if m.to == ["team@example.com"]]
        self.assertEqual(len(team_copy), 1)
        self.assertIn("New time", team_copy[0].body)
        self.assertIn("Member User <member@example.com>", team_copy[0].body)

    def test_action_requires_change_permission(self):
        print("\ntest_action_requires_change_permission")
        viewer = User.objects.create_user(
            username="viewer", password="testpassword", is_staff=True
        )
        self.client.force_login(viewer)
        self.post(stage="send", subject="Change", message="New time")
        self.assertEqual(len(mail.outbox), 0)
