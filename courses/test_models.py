from datetime import date, datetime, time, timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase

from fees.models import Fee
from .models import AccommodationOption, Course, CourseSession, InternalCourse


class TestCourseModel(TestCase):
    """Tests for the Course model"""

    def setUp(self):
        self.valid_course = InternalCourse.objects.create(
            title="Valid course",
            slug="valid-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.invalid_coures = InternalCourse.objects.create(
            title="Invalid course",
            slug="invalid-course",
            start_date=date.today(),
            end_date=date.today() - timedelta(days=1),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )

    def test_course_str_method_returns_title(self):
        print("\ntest_course_str_method_returns_title")
        course = InternalCourse.objects.get(translations__title="Valid course")
        self.assertEqual(str(course), "Valid course")

    def test_course_custom_date_validation(self):
        print("\ntest_course_custom_date_validation")
        course = InternalCourse.objects.get(translations__title="Invalid course")
        # https://stackoverflow.com/questions/73188838/django-testcase-
        # check-validationerror-with-assertraises-in-is-throwing-validatio
        self.assertRaises(ValidationError, course.clean)

    def test_registration_dates_validation(self):
        print("\ntest_registration_dates_validation")
        # Create course with invalid registration dates
        course = InternalCourse.objects.create(
            title="Bad registration dates",
            slug="bad-reg-dates",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=10),
            registration_start_date=date.today() + timedelta(days=5),
            registration_end_date=date.today() + timedelta(days=1),  # before start
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.assertRaises(ValidationError, course.clean)

    def test_missing_fee_validation(self):
        print("\ntest_missing_fee_validation")
        # Create course with non-existent fee combination
        course = InternalCourse.objects.create(
            title="Invalid fee combo",
            slug="invalid-fee-combo",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="non_existent_type",
            fee_category="non_existent_category",
        )
        self.assertRaises(ValidationError, course.clean)

    def test_dan_discount_validation(self):
        print("\ntest_dan_discount_validation")
        # Create non-international course with DAN discount (should fail)
        course = InternalCourse.objects.create(
            title="Invalid DAN discount",
            slug="invalid-dan-discount",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="dan_bw_teacher",
            fee_category="regular",
            dan_discount=True,
        )
        self.assertRaises(ValidationError, course.clean)

        # Create dan_seminar course with DAN discount (should also fail)
        course2 = InternalCourse.objects.create(
            title="Invalid DAN discount seminar",
            slug="invalid-dan-discount-seminar",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="dan_seminar",
            dan_discount=True,
        )
        self.assertRaises(ValidationError, course2.clean)

    def test_children_course_registration_validation(self):
        print("\ntest_children_course_registration_validation")
        # Create children's course with open registration (should fail)
        course = InternalCourse.objects.create(
            title="Children course",
            slug="children-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="children",
            fee_category="regular",
            registration_status=1,
        )
        self.assertRaises(ValidationError, course.clean)


class TestCourseBusinessLogic(TestCase):
    """Tests for Course model business logic"""

    def test_slug_collision_handling(self):
        print("\ntest_slug_collision_handling")
        # Create first course
        course1 = InternalCourse.objects.create(
            title="Duplicate Title",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.assertEqual(course1.slug, "duplicate-title")

        # Create second course with same title
        course2 = InternalCourse.objects.create(
            title="Duplicate Title",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.assertEqual(course2.slug, "duplicate-title-1")

        # Create third course with same title
        course3 = InternalCourse.objects.create(
            title="Duplicate Title",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.assertEqual(course3.slug, "duplicate-title-2")

    def test_auto_registration_status_update(self):
        print("\ntest_auto_registration_status_update")
        # Course with valid registration window (should auto-open)
        course = InternalCourse.objects.create(
            title="Auto open registration",
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=31),
            registration_start_date=date.today() - timedelta(days=1),
            registration_end_date=date.today() + timedelta(days=10),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.assertEqual(course.registration_status, 1)  # Should be open

        # Course with past registration window (should auto-close)
        course2 = InternalCourse.objects.create(
            title="Auto close registration",
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=31),
            registration_start_date=date.today() - timedelta(days=10),
            registration_end_date=date.today() - timedelta(days=1),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.assertEqual(course2.registration_status, 0)  # Should be closed

    def test_auto_publish_on_publication_date(self):
        print("\ntest_auto_publish_on_publication_date")
        # Course with publication date in the past (should auto-publish)
        course = InternalCourse.objects.create(
            title="Auto publish",
            start_date=date.today() + timedelta(days=10),
            end_date=date.today() + timedelta(days=11),
            publication_date=date.today() - timedelta(days=1),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
            status=0,  # Start as preview
        )
        self.assertEqual(course.status, 1)  # Should be published

    def test_auto_reset_has_dan_preparation(self):
        print("\ntest_auto_reset_has_dan_preparation")
        # Course with has_dan_preparation=True but wrong course type
        course = InternalCourse.objects.create(
            title="Wrong DAN prep type",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="children",  # Not in DAN_PREPARATION_COURSES
            fee_category="children",
            has_dan_preparation=True,
        )
        self.assertEqual(course.has_dan_preparation, False)  # Should be reset

    def test_update_has_dan_preparation(self):
        print("\ntest_update_has_dan_preparation")
        # Create a DAN preparation eligible course
        course = InternalCourse.objects.create(
            title="DAN prep course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="family_reunion",  # In DAN_PREPARATION_COURSES
            fee_category="dan_member",
            has_dan_preparation=False,
        )

        # Add a DAN preparation session
        session = CourseSession.objects.create(
            title="DAN Prep Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_dan_preparation=True,
        )

        # Refresh course from DB
        course.refresh_from_db()
        self.assertEqual(course.has_dan_preparation, True)  # Should be updated


class TestCourseSessionModel(TestCase):
    """Tests for the CourseSession model"""

    def setUp(self):
        self.course = InternalCourse.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.course_sessions = []
        for i in range(2):
            session = CourseSession.objects.create(
                title=f"Test session {i}",
                course=self.course,
                date=date.today(),
                start_time=datetime.now().time(),
                end_time=(datetime.now() + timedelta(hours=1)).time(),
            )
            self.course_sessions.append(session)

        self.invalid_session = CourseSession.objects.create(
            title="Invalid session",
            course=self.course,
            date=date.today(),
            start_time=time(10, 0, 0),
            end_time=time(9, 0, 0),
        )

    def test_session_str_method_returns_title(self):
        print("\ntest_session_str_method_returns_title")
        counter = 0
        for session in self.course_sessions:
            # __str__ returns formatted date/time with title, check it contains the title
            self.assertIn(f"Test session {counter}", str(session))
            counter += 1

    def test_session_custom_date_validation(self):
        print("\ntest_session_custom_date_validation")
        session = CourseSession.objects.get(translations__title="Invalid session")
        self.assertRaises(ValidationError, session.clean)

    def test_session_dan_preparation_validation(self):
        print("\ntest_session_dan_preparation_validation")
        # Try to add DAN preparation session to non-DAN course type
        invalid_session = CourseSession.objects.create(
            title="Invalid DAN prep",
            course=self.course,  # dan_bw_teacher not in DAN_PREPARATION_COURSES
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_dan_preparation=True,  # Should fail validation
        )
        self.assertRaises(ValidationError, invalid_session.clean)


class TestAccommodationOption(TestCase):
    """Tests for the AccommodationOption model"""

    def test_accommodation_option_str(self):
        print("\ntest_accommodation_option_str")
        # Create a course
        course = InternalCourse.objects.create(
            title="Test course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="family_reunion",
            fee_category="dan_member",
        )

        # Create accommodation option
        option = AccommodationOption.objects.create(
            course=course,
            name="2 Nights",
            fee=50.00,
        )

        self.assertEqual(str(option), "2 Nights (50.0€)")
