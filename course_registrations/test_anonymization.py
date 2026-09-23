from datetime import date
from decimal import Decimal
from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from courses.models import CourseSession, InternalCourse
from users.models import User, UserProfile

from .models import CourseRegistration


def create_course(year, slug):
    return InternalCourse.objects.create(
        title=f"Course {year}",
        slug=slug,
        start_date=date(year, 5, 1),
        end_date=date(year, 5, 2),
        course_type="sensei_emmerson",
        fee_category="regular",
    )


def create_guest_registration(course, name="Guest"):
    registration = CourseRegistration.objects.create(
        course=course, first_name=name, last_name="Person",
        email=f"{name.lower()}@example.com", comment="Vegetarian",
        grade=3, exam=True, exam_grade=4, discount=True, dan_member=True,
        final_fee=Decimal("45.00"), payment_status=1, dojo="Aikido Dojo",
        accept_terms=True,
    )
    return registration


def create_user_registration(course, username, is_active=True):
    user = User.objects.create_user(
        username=username, password="testpassword", email=f"{username}@example.com",
        first_name=username, last_name="Member", is_active=is_active,
    )
    UserProfile.objects.create(user=user, dojo="AAR", grade=2)
    return CourseRegistration.objects.create(course=course, user=user, accept_terms=True)


class DueForAnonymizationTest(TestCase):
    """Tests for CourseRegistration.due_for_anonymization"""

    today = date(2027, 1, 15)

    def setUp(self):
        self.course_2025 = create_course(2025, "course-2025")
        self.course_2026 = create_course(2026, "course-2026")

    def test_guest_registrations_two_calendar_years_old_are_due(self):
        print("\ntest_guest_registrations_two_calendar_years_old_are_due")
        old = create_guest_registration(self.course_2025)
        create_guest_registration(self.course_2026)
        due = CourseRegistration.due_for_anonymization(self.today)
        self.assertEqual(list(due), [old])

    def test_active_account_registrations_are_kept(self):
        print("\ntest_active_account_registrations_are_kept")
        create_user_registration(self.course_2025, "active")
        self.assertFalse(CourseRegistration.due_for_anonymization(self.today).exists())

    def test_deactivated_account_registrations_are_due(self):
        print("\ntest_deactivated_account_registrations_are_due")
        registration = create_user_registration(self.course_2025, "gone", is_active=False)
        due = CourseRegistration.due_for_anonymization(self.today)
        self.assertEqual(list(due), [registration])

    def test_already_anonymized_registrations_are_not_due(self):
        print("\ntest_already_anonymized_registrations_are_not_due")
        create_guest_registration(self.course_2025).anonymize(self.today)
        self.assertFalse(CourseRegistration.due_for_anonymization(self.today).exists())


class AnonymizeTest(TestCase):
    """Tests for CourseRegistration.anonymize"""

    def setUp(self):
        self.course = create_course(2024, "course-2024")
        self.session = CourseSession.objects.create(
            course=self.course, title="Session", date=date(2024, 5, 1),
            start_time="10:00", end_time="12:00",
        )

    def test_removes_personal_data_and_keeps_course_and_fees(self):
        print("\ntest_removes_personal_data_and_keeps_course_and_fees")
        registration = create_guest_registration(self.course)
        registration.selected_sessions.add(self.session)
        registration.anonymize(date(2026, 1, 1))
        registration.refresh_from_db()

        for field in ("user", "first_name", "last_name", "email", "grade",
                      "exam_grade", "exam_passed"):
            self.assertIsNone(getattr(registration, field), field)
        self.assertEqual(registration.comment, "")
        self.assertFalse(registration.exam)
        self.assertFalse(registration.discount)
        self.assertFalse(registration.dan_member)
        self.assertEqual(registration.anonymized_on, date(2026, 1, 1))
        self.assertEqual(str(registration), "Anonymisiert")

        self.assertEqual(registration.course, self.course)
        self.assertEqual(list(registration.selected_sessions.all()), [self.session])
        self.assertEqual(registration.final_fee, Decimal("45.00"))
        self.assertEqual(registration.payment_status, 1)
        self.assertEqual(registration.dojo, "Aikido Dojo")

    def test_several_anonymized_registrations_for_same_course(self):
        print("\ntest_several_anonymized_registrations_for_same_course")
        for name in ("One", "Two"):
            create_guest_registration(self.course, name).anonymize()
        self.assertEqual(
            CourseRegistration.objects.filter(anonymized_on__isnull=False).count(), 2
        )

    def test_deactivated_account_is_unlinked(self):
        print("\ntest_deactivated_account_is_unlinked")
        registration = create_user_registration(self.course, "gone", is_active=False)
        registration.anonymize()
        registration.refresh_from_db()
        self.assertIsNone(registration.user)
        self.assertIsNone(registration.email)
        self.assertIsNone(registration.grade)


class AnonymizeRegistrationsCommandTest(TestCase):
    """Tests for the anonymize_registrations management command"""

    def setUp(self):
        old_course = create_course(date.today().year - 2, "old-course")
        recent_course = create_course(date.today().year - 1, "recent-course")
        self.old = create_guest_registration(old_course)
        self.recent = create_guest_registration(recent_course)

    def test_dry_run_changes_nothing(self):
        print("\ntest_dry_run_changes_nothing")
        out = StringIO()
        call_command("anonymize_registrations", "--dry-run", stdout=out)
        self.assertIn(f"{date.today().year - 2}: 1 registrations", out.getvalue())
        self.old.refresh_from_db()
        self.assertIsNone(self.old.anonymized_on)

    def test_anonymizes_only_due_registrations(self):
        print("\ntest_anonymizes_only_due_registrations")
        call_command("anonymize_registrations", stdout=StringIO())
        self.old.refresh_from_db()
        self.recent.refresh_from_db()
        self.assertIsNotNone(self.old.anonymized_on)
        self.assertIsNone(self.recent.anonymized_on)
        self.assertEqual(self.recent.first_name, "Guest")
