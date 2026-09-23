import os
from datetime import date, datetime, timedelta
from unittest.mock import patch

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from courses.models import CourseSession, InternalCourse
from danbw_website import constants, utils
from users.models import User, UserProfile

from .models import CourseRegistration


def create_course(slug, starts_in_days):
    start = date.today() + timedelta(days=starts_in_days)
    course = InternalCourse.objects.create(
        title=f"Course {slug}",
        slug=slug,
        start_date=start,
        end_date=start + timedelta(days=1),
        registration_status=1,
        course_type="external_teacher",
        fee_category="regular",
        discount_percentage=0,
    )
    sessions = [
        CourseSession.objects.create(
            title=f"Session {n}", course=course, date=start,
            start_time=datetime.now().time(), end_time=datetime.now().time(),
        )
        for n in (1, 2)
    ]
    return course, sessions


def create_guest_registration(course, sessions, dojo="Other Club"):
    registration = CourseRegistration.objects.create(
        course=course, first_name="Guest", last_name="Person",
        email="guest@example.com", dojo=dojo, grade=3, accept_terms=True,
    )
    registration.selected_sessions.set(sessions)
    return registration


def guest_url(name, registration):
    return reverse(name, kwargs={"token": registration.get_manage_token()})


@patch.dict(os.environ, {"COURSE_TEAM_EMAIL": "team@example.com"})
class GuestSelfServiceTest(TestCase):
    """Tests for managing guest registrations via the personal link"""
    fixtures = ["fees.json"]

    def setUp(self):
        self.course, self.sessions = create_course("upcoming", starts_in_days=7)
        self.registration = create_guest_registration(self.course, self.sessions[:1])

    def update_data(self, **overrides):
        data = {
            "first_name": "Guest",
            "last_name": "Person",
            "email": "guest@example.com",
            "grade": 3,
            "dojo": "other",
            "other_dojo": "Other Club",
            "selected_sessions": [s.id for s in self.sessions],
            "accept_terms": True,
            "payment_method": 0,
        }
        data.update(overrides)
        return data

    def test_personal_link_shows_registration(self):
        print("\ntest_personal_link_shows_registration")
        response = self.client.get(guest_url("guest_registration", self.registration))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "guest_registration.html")
        self.assertContains(response, self.course.title)
        self.assertContains(response, guest_url("guest_cancel_courseregistration", self.registration))

    def test_invalid_token_returns_404(self):
        print("\ntest_invalid_token_returns_404")
        token = self.registration.get_manage_token() + "x"
        response = self.client.get(reverse("guest_registration", kwargs={"token": token}))
        self.assertEqual(response.status_code, 404)

    def test_token_does_not_work_for_account_registrations(self):
        print("\ntest_token_does_not_work_for_account_registrations")
        user = User.objects.create_user(username="member", password="pw", email="m@example.com")
        UserProfile.objects.create(user=user, dojo="AAR")
        registration = CourseRegistration.objects.create(course=self.course, user=user, accept_terms=True)
        response = self.client.get(guest_url("guest_registration", registration))
        self.assertEqual(response.status_code, 404)

    def test_token_does_not_work_for_anonymized_registrations(self):
        print("\ntest_token_does_not_work_for_anonymized_registrations")
        url = guest_url("guest_registration", self.registration)
        self.registration.anonymize()
        self.assertEqual(self.client.get(url).status_code, 404)

    def test_update_form_shows_guest_fields_even_when_someone_is_logged_in(self):
        print("\ntest_update_form_shows_guest_fields_even_when_someone_is_logged_in")
        user = User.objects.create_user(username="other", password="pw", email="loggedin@example.com")
        UserProfile.objects.create(user=user, dojo="AAR")
        self.client.force_login(user)
        response = self.client.get(guest_url("guest_update_courseregistration", self.registration))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="first_name"')
        self.assertNotContains(response, "loggedin@example.com")
        form = response.context["form"]
        self.assertEqual(form.initial["dojo"], "other")
        self.assertEqual(form.initial["other_dojo"], "Other Club")

    def test_update_form_maps_known_dojo_to_choice(self):
        print("\ntest_update_form_maps_known_dojo_to_choice")
        self.registration.dojo = utils.get_tuple_value(constants.DOJO_CHOICES, "AAR")
        self.registration.save()
        response = self.client.get(guest_url("guest_update_courseregistration", self.registration))
        self.assertEqual(response.context["form"].initial["dojo"], "AAR")

    def test_update_saves_and_sends_confirmation_and_notification(self):
        print("\ntest_update_saves_and_sends_confirmation_and_notification")
        response = self.client.post(
            guest_url("guest_update_courseregistration", self.registration), self.update_data()
        )
        self.assertRedirects(
            response, guest_url("guest_registration", self.registration),
            fetch_redirect_response=False,
        )
        self.registration.refresh_from_db()
        self.assertEqual(self.registration.selected_sessions.count(), 2)

        confirmation = [m for m in mail.outbox if m.to == ["guest@example.com"]]
        notification = [m for m in mail.outbox if m.to == ["team@example.com"]]
        self.assertEqual(len(confirmation), 1)
        self.assertEqual(len(notification), 1)
        self.assertIn(guest_url("guest_registration", self.registration), confirmation[0].body)
        self.assertIn("Guest", notification[0].body)

    def test_cancel_deletes_and_notifies_team(self):
        print("\ntest_cancel_deletes_and_notifies_team")
        response = self.client.post(guest_url("guest_cancel_courseregistration", self.registration))
        self.assertRedirects(response, reverse("course_list"), fetch_redirect_response=False)
        self.assertFalse(CourseRegistration.objects.filter(pk=self.registration.pk).exists())
        self.assertEqual([m.to for m in mail.outbox], [["team@example.com"]])
        self.assertIn("guest@example.com", mail.outbox[0].body)

    def test_no_changes_once_the_course_has_started(self):
        print("\ntest_no_changes_once_the_course_has_started")
        course, sessions = create_course("started", starts_in_days=0)
        registration = create_guest_registration(course, sessions[:1])

        response = self.client.get(guest_url("guest_update_courseregistration", registration))
        self.assertRedirects(
            response, guest_url("guest_registration", registration), fetch_redirect_response=False
        )
        self.client.post(guest_url("guest_update_courseregistration", registration), self.update_data())
        self.client.post(guest_url("guest_cancel_courseregistration", registration))

        registration.refresh_from_db()
        self.assertEqual(registration.selected_sessions.count(), 1)
        self.assertEqual(len(mail.outbox), 0)

        page = self.client.get(guest_url("guest_registration", registration))
        self.assertNotContains(page, guest_url("guest_cancel_courseregistration", registration))


@patch.dict(os.environ, {"COURSE_TEAM_EMAIL": "team@example.com"})
class AccountHolderDeadlineTest(TestCase):
    """Account holders can no longer cancel or update once the course started"""
    fixtures = ["fees.json"]

    def setUp(self):
        self.user = User.objects.create_user(
            username="member", password="pw", email="member@example.com",
            first_name="Member", last_name="User",
        )
        UserProfile.objects.create(user=self.user, dojo="AAR", grade=2)
        self.client.force_login(self.user)

    def register(self, starts_in_days):
        course, sessions = create_course(f"course-{starts_in_days}", starts_in_days)
        registration = CourseRegistration.objects.create(course=course, user=self.user, accept_terms=True)
        registration.selected_sessions.set(sessions[:1])
        return registration

    def test_cannot_cancel_started_course(self):
        print("\ntest_cannot_cancel_started_course")
        registration = self.register(starts_in_days=0)
        self.client.post(reverse("cancel_courseregistration", kwargs={"pk": registration.pk}))
        self.assertTrue(CourseRegistration.objects.filter(pk=registration.pk).exists())

    def test_cannot_update_started_course(self):
        print("\ntest_cannot_update_started_course")
        registration = self.register(starts_in_days=-1)
        response = self.client.get(reverse("update_courseregistration", kwargs={"pk": registration.pk}))
        self.assertRedirects(response, reverse("courseregistration_list"), fetch_redirect_response=False)

    def test_update_sends_confirmation_without_personal_link(self):
        print("\ntest_update_sends_confirmation_without_personal_link")
        registration = self.register(starts_in_days=7)
        self.client.post(
            reverse("update_courseregistration", kwargs={"pk": registration.pk}),
            {
                "selected_sessions": [s.id for s in registration.course.sessions.all()],
                "accept_terms": True,
                "payment_method": 0,
            },
        )
        confirmation = [m for m in mail.outbox if m.to == ["member@example.com"]]
        self.assertEqual(len(confirmation), 1)
        self.assertIn("Member", confirmation[0].body)
        self.assertNotIn("/registration/", confirmation[0].body)
        self.assertEqual(len([m for m in mail.outbox if m.to == ["team@example.com"]]), 1)

    def test_list_hides_buttons_for_started_course(self):
        print("\ntest_list_hides_buttons_for_started_course")
        registration = self.register(starts_in_days=0)
        response = self.client.get(reverse("courseregistration_list"))
        self.assertNotContains(
            response, reverse("cancel_courseregistration", kwargs={"pk": registration.pk})
        )


@patch.dict(os.environ, {"COURSE_TEAM_EMAIL": "team@example.com"})
class GuestConfirmationLinkTest(TestCase):
    """New guest registrations get the personal link in their confirmation"""
    fixtures = ["fees.json"]

    def test_guest_confirmation_contains_personal_link(self):
        print("\ntest_guest_confirmation_contains_personal_link")
        course, sessions = create_course("new", starts_in_days=7)
        session = self.client.session
        session["captcha_target"] = "1"
        session.save()
        self.client.post(
            reverse("register_course", kwargs={"slug": course.slug}),
            {
                "first_name": "New", "last_name": "Guest", "email": "new@example.com",
                "grade": 3, "dojo": "AAR", "selected_sessions": [sessions[0].id],
                "accept_terms": True, "payment_method": 0, "captcha_response": "1",
            },
        )
        registration = CourseRegistration.objects.get(email="new@example.com")
        confirmation = [m for m in mail.outbox if m.to == ["new@example.com"]]
        self.assertEqual(len(confirmation), 1)
        self.assertIn(guest_url("guest_registration", registration), confirmation[0].body)
