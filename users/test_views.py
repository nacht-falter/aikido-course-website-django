from datetime import date, timedelta

from django.contrib.messages import get_messages
from django.test import TestCase

from .course_registrations.models import CourseRegistration
from .courses.models import Course
from .models import User, UserProfile


class UserProfileViewTest(TestCase):
    """Tests for UserProfileView view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="test-user",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_get_user_profile(self):
        print("\ntest_get_user_profile")
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            grade=0,
        )
        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "userprofile.html")

    def test_get_user_profile_form(self):
        print("\ntest_get_user_profile_form")
        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_userprofile.html")

    def test_post_valid_user_profile_form(self):
        print("\ntest_post_valid_user_profile_form")
        response = self.client.post(
            "/user/profile/",
            {
                "username": "test_username",
                "first_name": "Test",
                "last_name": "User",
                "email": "test@mail.com",
                "grade": 0,
            },
        )
        self.assertRedirects(response, "/user/profile/", 302, 200)

    def test_post_invalid_user_profile_form(self):
        print("\ntest_post_invalid_user_profile_form")
        response = self.client.post("/user/profile/")
        self.assertRedirects(response, "/user/profile/", 302, 200)


class UpdateUserProfileViewTest(TestCase):
    """Tests for UpdateUserProfile view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="test-username",
            password="testpassword",
            first_name="Test",
            last_name="User",
            email="test@mail.com",
        )
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.create(user=self.user, grade=0)

    def test_get_update_user_profile_form(self):
        print("\ntest_get_update_user_profile_form")
        response = self.client.get("/user/profile/update/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_userprofile.html")

    def test_post_valid_update_user_profile_form(self):
        print("\ntest_post_valid_update_user_profile_form")
        changed_data = {
            "username": "test_username_changed",
            "first_name": "Test_changed",
            "last_name": "User_changed",
            "email": "test_changed@mail.com",
            "grade": 1,
        }
        response = self.client.post("/user/profile/update/", changed_data)
        user_profile = UserProfile.objects.get(user=self.user)
        user = user_profile.user

        self.assertRedirects(response, "/user/profile/", 302, 200)
        self.assertEqual(user_profile.user.username, changed_data["username"])
        self.assertEqual(user.first_name, changed_data["first_name"])
        self.assertEqual(user.last_name, changed_data["last_name"])
        self.assertEqual(user.email, changed_data["email"])
        self.assertEqual(user_profile.grade, changed_data["grade"])

    def test_post_invalid_user_profile_form(self):
        print("\ntest_post_invalid_user_update_profile_form")
        response = self.client.post("/user/profile/update/")
        self.assertRedirects(response, "/user/profile/", 302, 200)


class DeactivateUserTest(TestCase):
    """Tests for DeactivateUser view"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="test-username",
            password="testpassword",
        )
        self.client.force_login(self.user)

    def test_get_deactivate_user(self):
        print("\ntest_get_deactivate_user")
        response = self.client.get("/user/deactivate/")
        self.assertRedirects(response, "/user/profile/", 302, 200)

    def test_post_deactivate_user(self):
        print("\ntest_post_deactivate_user")
        response = self.client.post("/user/deactivate/")
        user = User.objects.get(pk=self.user.pk)
        self.assertRedirects(response, "/courses/", 302, 200)
        self.assertFalse(user.is_active)

    def test_deactivate_staff_user(self):
        print("\ntest_deactivate_staff_user")
        user = User.objects.get(pk=self.user.pk)
        user.is_staff = True
        user.save()
        response = self.client.post("/user/deactivate/")
        self.assertRedirects(response, "/user/profile/", 302, 200)

        # Test messages: https://stackoverflow.com/a/46865530
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Staff accounts can not be deactivated."
            " Please contact us if you want to deactivate your account.",
            messages,
        )


class UpdateGradeTest(TestCase):
    """Tests for UpdateGrade view"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today() - timedelta(days=2),
            end_date=date.today() - timedelta(days=1),
            registration_status=(1),
            course_fee=50,
        )
        self.user = User.objects.create_user(
            username="test-user", password="testpassword"
        )
        self.user_profile = UserProfile.objects.create(user=self.user, grade=1)
        self.client.force_login(self.user)
        self.registration = CourseRegistration.objects.create(
            user=self.user,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=True,
            exam_grade=self.user_profile.grade + 1,
            grade_updated=False,
            comment="Test comment",
        )

    def test_get_update_grade_after_course(self):
        print("\ntest_get_update_grade_after_course")
        response = self.client.get("/user/update-grade/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_grade.html")

    def test_get_update_grade_before_course_ends(self):
        print("\ntest_get_update_grade_before_course_ends")
        self.course.end_date = date.today() + timedelta(days=1)
        self.course.save()
        response = self.client.get("/user/update-grade/")
        self.assertRedirects(response, "/", 302, 200)

    def test_post_update_grade_confirmed(self):
        print("\ntest_post_update_grade_confirmed")
        response = self.client.post("/user/update-grade/", {"answer": "yes"})
        self.registration.refresh_from_db()
        self.user_profile.refresh_from_db()
        self.assertEqual(self.user_profile.grade, self.registration.exam_grade)
        self.assertEqual(self.registration.grade_updated, True)
        self.assertRedirects(response, "/", 302, 200)

    def test_post_update_grade_cancelled(self):
        print("\ntest_post_update_grade_cancelled")
        response = self.client.post("/user/update-grade/", {"answer": "no"})
        self.registration.refresh_from_db()
        self.user_profile.refresh_from_db()
        self.assertEqual(
            self.user_profile.grade, self.registration.exam_grade - 1
        )
        self.assertEqual(self.registration.grade_updated, True)
        self.assertRedirects(response, "/", 302, 200)
