import csv
import io
import zipfile
from datetime import date, timedelta

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from course_registrations.models import CourseRegistration
from users.models import User, UserProfile

from .admin import ExternalCourseAdmin, InternalCourseAdmin
from .models import CourseSession, ExternalCourse, InternalCourse


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
            first_name="Test",
            last_name="User",
            email="test@example.com",
            final_fee=50,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )

    def test_duplicate_course_action(self):
        print("\ntest_duplicate_course_action")
        queryset = InternalCourse.objects.filter(translations__title="Test course")
        for i in range(2):
            self.admin.duplicate_selected_courses(request, queryset)

        first_copy = InternalCourse.objects.get(translations__title="Copy of Test course")
        second_copy = InternalCourse.objects.get(translations__title="Copy 2 of Test course")
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

    def test_courses_by_year_filter(self):
        print("\ntest_courses_by_year_filter")
        # Create courses in different years
        course_2023 = InternalCourse.objects.create(
            title="Course 2023",
            slug="course-2023",
            start_date=date(2023, 5, 15),
            end_date=date(2023, 5, 16),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        course_2024 = InternalCourse.objects.create(
            title="Course 2024",
            slug="course-2024",
            start_date=date(2024, 6, 20),
            end_date=date(2024, 6, 21),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )

        # Import and test the filter
        from .admin import CoursesByYearFilter

        # Test lookups() method
        course_filter = CoursesByYearFilter(request, {}, InternalCourse, self.admin)
        lookups = course_filter.lookups(request, self.admin)
        years = [lookup[0] for lookup in lookups]
        self.assertIn(2023, years)
        self.assertIn(2024, years)

        # Test queryset() method with a specific year
        # Note: Django admin expects parameter values as lists (from QueryDict)
        course_filter = CoursesByYearFilter(
            request, {"year": ["2023"]}, InternalCourse, self.admin
        )
        filtered_queryset = course_filter.queryset(
            request, InternalCourse.objects.all()
        )
        # Should only return courses from 2023
        filtered_count = filtered_queryset.filter(start_date__year=2023).count()
        self.assertGreater(filtered_count, 0)
        self.assertIn(course_2023, filtered_queryset)

    def test_future_course_filter(self):
        print("\ntest_future_course_filter")
        # Create past and future courses
        past_course = InternalCourse.objects.create(
            title="Past Course",
            slug="past-course",
            start_date=date.today() - timedelta(days=30),
            end_date=date.today() - timedelta(days=29),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        future_course = InternalCourse.objects.create(
            title="Future Course",
            slug="future-course",
            start_date=date.today() + timedelta(days=30),
            end_date=date.today() + timedelta(days=31),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )

        # Import and test the filter
        from .admin import FutureCourseFilter

        # Test lookups() method
        course_filter = FutureCourseFilter(request, {}, InternalCourse, self.admin)
        lookups = course_filter.lookups(request, self.admin)
        self.assertEqual(len(lookups), 2)
        self.assertEqual(lookups[0][0], "future")
        self.assertEqual(lookups[1][0], "past")

        # Test queryset() with "future" filter
        course_filter = FutureCourseFilter(
            request, {"future_course": ["future"]}, InternalCourse, self.admin
        )
        filtered_queryset = course_filter.queryset(
            request, InternalCourse.objects.all()
        )
        # Verify the filter returns a queryset and filters correctly
        self.assertIsNotNone(filtered_queryset)
        self.assertGreater(filtered_queryset.count(), 0)
        self.assertIn(future_course, filtered_queryset)
        self.assertNotIn(past_course, filtered_queryset)

        # Test queryset() with "past" filter
        course_filter = FutureCourseFilter(
            request, {"future_course": ["past"]}, InternalCourse, self.admin
        )
        filtered_queryset = course_filter.queryset(
            request, InternalCourse.objects.all()
        )
        # Verify the filter returns a queryset and filters correctly
        self.assertIsNotNone(filtered_queryset)
        self.assertGreater(filtered_queryset.count(), 0)
        self.assertIn(past_course, filtered_queryset)
        self.assertNotIn(future_course, filtered_queryset)

    def test_toggle_status_action(self):
        print("\ntest_toggle_status_action")
        # Create a course with status=True (published)
        published_course = InternalCourse.objects.create(
            title="Published Course",
            slug="published-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
            status=True,
        )

        # Toggle status to False (draft)
        queryset = InternalCourse.objects.filter(id=published_course.id)
        self.admin.toggle_status(request, queryset)
        published_course.refresh_from_db()
        self.assertEqual(published_course.status, False)

        # Toggle back to True (published)
        self.admin.toggle_status(request, queryset)
        published_course.refresh_from_db()
        self.assertEqual(published_course.status, True)

    def test_export_csv_single_course(self):
        print("\ntest_export_csv_single_course")
        # Export single course (self.course from setUp already has a registration)
        queryset = InternalCourse.objects.filter(id=self.course.id)
        response = self.admin.export_csv(request, queryset)

        # Verify response is CSV
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn("attachment", response["Content-Disposition"])
        self.assertIn("test-course", response["Content-Disposition"])

        # Verify CSV contains registration data
        content = response.content.decode("utf-8")
        csv_reader = csv.reader(io.StringIO(content))
        rows = list(csv_reader)

        # Should have at least 2 rows (header + 1 registration)
        self.assertGreaterEqual(len(rows), 2)

        # Check that registration data is in CSV
        csv_content = "\n".join([",".join(row) for row in rows])
        self.assertIn("test course", csv_content.lower())
        self.assertIn("test comment", csv_content.lower())

    def test_export_csv_multiple_courses(self):
        print("\ntest_export_csv_multiple_courses")
        # Create a second course with a registration
        course2 = InternalCourse.objects.create(
            title="Test course 2",
            slug="test-course-2",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=0,
            course_type="dan_bw_teacher",
            fee_category="dan_member",
        )
        registration2 = CourseRegistration.objects.create(
            user=self.user,
            course=course2,
            first_name="Test",
            last_name="User",
            email="test@example.com",
            final_fee=60,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment 2",
        )

        # Export multiple courses
        queryset = InternalCourse.objects.filter(
            id__in=[self.course.id, course2.id]
        )
        response = self.admin.export_csv(request, queryset)

        # Verify response is ZIP
        self.assertEqual(response["Content-Type"], "application/zip")
        self.assertIn("attachment", response["Content-Disposition"])

        # Verify ZIP contains CSV files
        zip_content = io.BytesIO(response.content)
        with zipfile.ZipFile(zip_content, "r") as zip_file:
            filenames = zip_file.namelist()
            self.assertEqual(len(filenames), 2)

            # Verify both courses are in the ZIP
            self.assertTrue(any("test-course" in f for f in filenames))
            self.assertTrue(any("test-course-2" in f for f in filenames))

    def test_duplicate_with_sessions(self):
        print("\ntest_duplicate_with_sessions")
        # Create sessions for the course
        session1 = CourseSession.objects.create(
            title="Session 1",
            course=self.course,
            date=date.today(),
            start_time="10:00",
            end_time="12:00",
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=self.course,
            date=date.today() + timedelta(days=1),
            start_time="14:00",
            end_time="16:00",
        )

        # Duplicate the course
        queryset = InternalCourse.objects.filter(id=self.course.id)
        self.admin.duplicate_selected_courses(request, queryset)

        # Get the duplicated course
        duplicated_course = InternalCourse.objects.get(translations__title="Copy of Test course")

        # Verify sessions were duplicated
        duplicated_sessions = duplicated_course.sessions.all()
        self.assertEqual(duplicated_sessions.count(), 2)
        # Access translated titles
        self.assertEqual(duplicated_sessions[0].title, "Session 1")
        self.assertEqual(duplicated_sessions[1].title, "Session 2")


class TestExternalCourseAdmin(TestCase):
    """Tests for the ExternalCourseAdmin model"""

    def setUp(self):
        site = AdminSite()
        self.admin = ExternalCourseAdmin(ExternalCourse, site)
        self.course = ExternalCourse.objects.create(
            title="Test external course",
            slug="test-external-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            url="https://example.com",
            organizer="Test Organizer",
            teacher="Test Teacher",
        )

    def test_external_course_duplicate(self):
        print("\ntest_external_course_duplicate")
        queryset = ExternalCourse.objects.filter(translations__title="Test external course")

        # First duplication
        self.admin.duplicate_selected_courses(request, queryset)
        first_copy = ExternalCourse.objects.get(translations__title="Copy of Test external course")
        self.assertTrue(first_copy)
        self.assertEqual(first_copy.slug, "copy-of-test-external-course")
        self.assertEqual(first_copy.url, "https://example.com")

        # Second duplication should create "Copy 2 of..."
        self.admin.duplicate_selected_courses(request, queryset)
        second_copy = ExternalCourse.objects.get(translations__title="Copy 2 of Test external course")
        self.assertTrue(second_copy)
        self.assertEqual(second_copy.slug, "copy-2-of-test-external-course")
