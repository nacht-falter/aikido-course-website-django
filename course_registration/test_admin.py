from django.contrib.admin.sites import AdminSite
from django.test import TestCase
from django.test import RequestFactory
from datetime import date, timedelta
from .models import Course
from .admin import CourseAdmin


# Testing Django admin instructions from: https://www.argpar.se/posts/programming/testing-django-admin
request_factory = RequestFactory()
request = request_factory.get("/admin")


class TestCourseAdmin(TestCase):
    """Tests for the CourseAdmin model"""

    def setUp(self):
        site = AdminSite()
        self.admin = CourseAdmin(Course, site)
        self.course = Course.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(0),
            course_fee=50,
        )

    def test_duplicate_course_action(self):
        print("\ntest_duplicate_course_action")
        queryset = Course.objects.filter(title="Test course")
        for i in range(2):
            self.admin.duplicate_selected_courses(request, queryset)

        first_copy = Course.objects.get(title="Copy of Test course")
        second_copy = Course.objects.get(title="Copy 2 of Test course")
        self.assertTrue(first_copy)
        self.assertTrue(second_copy)
        self.assertEqual(first_copy.slug, "copy-of-test-course")
        self.assertEqual(second_copy.slug, "copy-2-of-test-course")
