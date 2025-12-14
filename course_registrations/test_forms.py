from datetime import date, timedelta, time

from django.core.exceptions import ValidationError
from django.test import TestCase

from courses.models import CourseSession, InternalCourse
from fees.models import Fee
from users.models import User, UserProfile

from .forms import CourseRegistrationForm


class TestCourseRegistrationFormValidation(TestCase):
    """Tests for CourseRegistrationForm validation logic"""

    def setUp(self):
        """Set up common test data"""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )

    def test_dan_seminar_low_grade_user_with_profile(self):
        """Test that users with grade <= 5 cannot register for dan_seminar"""
        print("\ntest_dan_seminar_low_grade_user_with_profile")

        # Create user profile with low grade (5 = 5th Kyu)
        user_profile = UserProfile.objects.create(
            user=self.user, dojo="AAR", grade=5
        )

        # Create dan_seminar course
        course = InternalCourse.objects.create(
            title="Dan Seminar",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Try to create form with low grade user
        form = CourseRegistrationForm(
            data={
                "selected_sessions": [session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
            course=course,
            user_profile=user_profile,
        )

        # Form should be invalid
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Du musst mindestens 1. Kyu sein, um Dich für diesen Lehrgang anmelden zu können.",
            str(form.errors),
        )

    def test_dan_seminar_high_grade_user_allowed(self):
        """Test that users with grade > 5 can register for dan_seminar"""
        print("\ntest_dan_seminar_high_grade_user_allowed")

        # Create user profile with high grade (6 = 1st Kyu)
        user_profile = UserProfile.objects.create(
            user=self.user, dojo="AAR", grade=6
        )

        # Create dan_seminar course
        course = InternalCourse.objects.create(
            title="Dan Seminar",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for dan_seminar
        Fee.objects.create(
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
            fee_type="single_day",
            amount=80.00,
        )

        # Try to create form with high grade user
        form = CourseRegistrationForm(
            data={
                "selected_sessions": [session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
            course=course,
            user_profile=user_profile,
        )

        # Form should be valid
        self.assertTrue(form.is_valid())

    def test_dan_seminar_low_grade_guest(self):
        """Test that guests with grade <= 5 cannot register for dan_seminar"""
        print("\ntest_dan_seminar_low_grade_guest")

        # Create dan_seminar course
        course = InternalCourse.objects.create(
            title="Dan Seminar",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Try to create form for guest with low grade (no user_profile)
        form = CourseRegistrationForm(
            data={
                "first_name": "Guest",
                "last_name": "User",
                "email": "guest@example.com",
                "dojo": "AAR",
                "grade": 5,  # 5th Kyu - too low
                "selected_sessions": [session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
            course=course,
            user_profile=None,  # Guest user
        )

        # Form should be invalid
        self.assertFalse(form.is_valid())
        self.assertIn(
            "Du musst mindestens 1. Kyu sein, um Dich für diesen Lehrgang anmelden zu können.",
            str(form.errors),
        )

    def test_dan_seminar_high_grade_guest_allowed(self):
        """Test that guests with grade > 5 can register for dan_seminar"""
        print("\ntest_dan_seminar_high_grade_guest_allowed")

        # Create dan_seminar course
        course = InternalCourse.objects.create(
            title="Dan Seminar",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for dan_seminar
        Fee.objects.create(
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
            fee_type="single_day",
            amount=80.00,
        )

        # Try to create form for guest with high grade
        form = CourseRegistrationForm(
            data={
                "first_name": "Guest",
                "last_name": "User",
                "email": "guest@example.com",
                "dojo": "AAR",
                "grade": 6,  # 1st Kyu - allowed
                "selected_sessions": [session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
            course=course,
            user_profile=None,  # Guest user
        )

        # Form should be valid
        self.assertTrue(form.is_valid())

    def test_dojo_other_without_other_dojo_field(self):
        """Test that selecting 'other' dojo without specifying other_dojo raises error"""
        print("\ntest_dojo_other_without_other_dojo_field")

        # Create regular course
        course = InternalCourse.objects.create(
            title="Regular Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Try to create form for guest with dojo="other" but no other_dojo
        form = CourseRegistrationForm(
            data={
                "first_name": "Guest",
                "last_name": "User",
                "email": "guest@example.com",
                "dojo": "other",  # Selected "other"
                "other_dojo": "",  # But didn't specify which
                "grade": 6,
                "selected_sessions": [session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
            course=course,
            user_profile=None,
        )

        # Form should be invalid
        self.assertFalse(form.is_valid())
        self.assertIn("other_dojo", form.errors)
        # Check for key parts of the error message (apostrophes may be HTML encoded)
        error_msg = str(form.errors["other_dojo"])
        self.assertIn("Bitte gib ein Dojo an", error_msg)
        self.assertIn("Anderes Dojo", error_msg)

    def test_dojo_other_with_other_dojo_specified(self):
        """Test that selecting 'other' dojo with other_dojo specified works"""
        print("\ntest_dojo_other_with_other_dojo_specified")

        # Create regular course
        course = InternalCourse.objects.create(
            title="Regular Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
        )

        # Try to create form for guest with dojo="other" AND other_dojo specified
        form = CourseRegistrationForm(
            data={
                "first_name": "Guest",
                "last_name": "User",
                "email": "guest@example.com",
                "dojo": "other",  # Selected "other"
                "other_dojo": "My Custom Dojo",  # Specified which one
                "grade": 6,
                "selected_sessions": [session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
            course=course,
            user_profile=None,
        )

        # Form should be valid
        self.assertTrue(form.is_valid())

        # Verify that dojo is set to the custom value
        self.assertEqual(form.cleaned_data["dojo"], "My Custom Dojo")

    def test_regular_dojo_selection(self):
        """Test that selecting a regular dojo works and gets display value"""
        print("\ntest_regular_dojo_selection")

        # Create regular course
        course = InternalCourse.objects.create(
            title="Regular Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
        )

        # Try to create form for guest with regular dojo selection
        form = CourseRegistrationForm(
            data={
                "first_name": "Guest",
                "last_name": "User",
                "email": "guest@example.com",
                "dojo": "AAR",  # Regular dojo choice
                "grade": 6,
                "selected_sessions": [session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
            course=course,
            user_profile=None,
        )

        # Form should be valid
        self.assertTrue(form.is_valid())

        # Verify that dojo is set to the display value
        self.assertEqual(form.cleaned_data["dojo"], "Aikido am Rhein")
