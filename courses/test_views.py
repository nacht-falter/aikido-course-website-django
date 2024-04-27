from datetime import date, datetime, timedelta

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core import mail

from .models import (
    Course,
    CourseRegistration,
    UserProfile,
    CourseSession,
    Category,
    Page,
)


class CourseListTest(TestCase):
    """Tests for CourseList view"""

    def setUp(self):
        self.number_of_courses = 3
        for i in range(self.number_of_courses):
            self.course = Course.objects.create(
                title=f"Course {i}",
                slug=f"course-{i}",
                start_date=date.today(),
                end_date=date.today() + timedelta(days=1),
                registration_status=(0),
                course_fee=50,
            )

    def test_course_list_view(self):
        print("\ntest_course_list_view")
        courses = Course.objects.all()
        response = self.client.get("/courses/")

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "course_list.html")
        self.assertEqual(len(courses), self.number_of_courses)

