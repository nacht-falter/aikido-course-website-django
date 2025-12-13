from datetime import date, datetime, timedelta

from django.contrib.messages import get_messages
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from course_registrations.models import CourseRegistration
from pages.models import Category, Page
from users.models import User, UserProfile

from .models import Course, CourseSession, InternalCourse


class CourseListTest(TestCase):
    """Tests for CourseList view"""

    def setUp(self):
        self.number_of_courses = 3
        for i in range(self.number_of_courses):
            self.course = InternalCourse.objects.create(
                title=f"Course {i}",
                slug=f"course-{i}",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=1),
                registration_status=(0),
                course_type="dan_bw_teacher",
                fee_category="dan_member",
            )

    def test_course_list_view(self):
        print("\ntest_course_list_view")
        courses = Course.objects.all()
        response = self.client.get(reverse("course_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course_list.html")
        self.assertEqual(len(courses), self.number_of_courses)

