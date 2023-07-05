from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta
from .models import Course, CourseSession


class TestCourseModel(TestCase):
    """Tests for the Course model"""

    def setUp(self):
        self.valid_course = Course.objects.create(
            title="Valid course",
            slug="valid-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(0),
            course_fee=50,
        )
        self.invalid_coures = Course.objects.create(
            title="Invalid course",
            slug="invalid-course",
            start_date=date.today(),
            end_date=date.today() - timedelta(days=1),
            registration_status=(0),
            course_fee=50,
        )

    def test_course_str_method_returns_title(self):
        print("\ntest_course_str_method_returns_title")
        course = Course.objects.get(title="Valid course")
        self.assertEqual(str(course), "Valid course")

    def test_course_custom_date_validation(self):
        print("\ntest_course_custom_date_validation")
        course = Course.objects.get(title="Invalid course")
        # https://stackoverflow.com/questions/73188838/django-testcase-check-validationerror-with-assertraises-in-is-throwing-validatio
        self.assertRaises(ValidationError, course.clean)


class TestCourseSessionModel(TestCase):
    """Tests for the CourseSession model"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(0),
            course_fee=50,
        )
        self.course_sessions = []
        for i in range(2):
            session = CourseSession.objects.create(
                title=f"Test session {i}",
                course=self.course,
                date=date.today(),
                start_time=datetime.now().time(),
                end_time=(datetime.now() + timedelta(hours=1)).time(),
                session_fee=10,
            )
            self.course_sessions.append(session)

        self.invalid_session = CourseSession.objects.create(
            title="Invalid session",
            course=self.course,
            date=date.today(),
            start_time=(datetime.now() + timedelta(hours=1)).time(),
            end_time=datetime.now().time(),
            session_fee=10,
        )

    def test_session_str_method_returns_date_and_title(self):
        print("\ntest_session_str_method_returns_title")
        expected_date = date.today()
        counter = 0
        for session in self.course_sessions:
            self.assertEqual(
                str(session), f"{expected_date}: Test session {counter}"
            )
            counter += 1

    def test_session_custom_date_validation(self):
        print("\ntest_session_custom_date_validation")
        session = CourseSession.objects.get(title="Invalid session")
        # https://stackoverflow.com/questions/73188838/django-testcase-check-validationerror-with-assertraises-in-is-throwing-validatio
        self.assertRaises(ValidationError, session.clean)
