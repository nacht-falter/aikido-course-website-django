from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import date, timedelta
from .models import Course


class TestCourseModel(TestCase):
    """Tests four the Course Model"""

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

    def test_custom_date_validation(self):
        print("\ntest_custom_date_validation")
        course = Course.objects.get(title="Invalid course")
        self.assertRaises(ValidationError, course.clean)
