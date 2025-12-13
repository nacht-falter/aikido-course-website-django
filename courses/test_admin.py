from datetime import date, timedelta

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from course_registrations.models import CourseRegistration
from users.models import User, UserProfile

from .admin import InternalCourseAdmin
from .models import InternalCourse


# Testing Django admin instructions from:
# https://www.argpar.se/posts/programming/testing-django-admin
request_factory = RequestFactory()
request = request_factory.get("/admin")


class TestCourseAdmin(TestCase):
    """Tests for the InternalCourseAdmin model"""

    def setUp(self):
        site = AdminSite()
        self.admin = InternalCourseAdmin(InternalCourse, site)
        self.course = InternalCourse.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        self.user = User.objects.create_user(
            username="test-user", password="testpassword"
        )
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.create(user=self.user)
        self.registration = CourseRegistration.objects.create(
            user=self.user,
            course=self.course,
            final_fee=50,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )

    def test_duplicate_course_action(self):
        print("\ntest_duplicate_course_action")
        queryset = InternalCourse.objects.filter(title="Test course")
        for i in range(2):
            self.admin.duplicate_selected_courses(request, queryset)

        first_copy = InternalCourse.objects.get(title="Copy of Test course")
        second_copy = InternalCourse.objects.get(title="Copy 2 of Test course")
        self.assertTrue(first_copy)
        self.assertTrue(second_copy)
        self.assertEqual(first_copy.slug, "copy-of-test-course")
        self.assertEqual(second_copy.slug, "copy-2-of-test-course")

    def test_get_course_registration_count(self):
        print("\ntest_get_course_registration_count")
        registrations = CourseRegistration.objects.filter(course=self.course)
        registration_count = self.admin.get_course_registration_count(
            self.course
        )
        self.assertEqual(len(registrations), registration_count)

    def test_toggle_registration_status_action(self):
        print("\ntest_toggle_registration_status_action")
        queryset = InternalCourse.objects.all()
        self.admin.toggle_registration_status(request, queryset)
        self.course.refresh_from_db()
        self.assertEqual(self.course.registration_status, 1)
        self.admin.toggle_registration_status(request, queryset)
        self.course.refresh_from_db()
        self.assertEqual(self.course.registration_status, 0)
