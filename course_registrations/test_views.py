from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.test import TestCase

from courses.models import Course, CourseSession
from users.models import UserProfile

from .models import UserCourseRegistration


class RegisterCourseTest(TestCase):
    """Tests for RegisterCourse view"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(1),
            course_fee=50,
        )
        self.session = CourseSession.objects.create(
            title="Test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )
        # Test user login:
        # https://docs.djangoproject.com/en/3.2/topics/testing/tools
        # /#django.test.Client.force_login
        self.user = User.objects.create_user(
            username="test-user", password="testpassword"
        )
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.create(user=self.user)

    def test_get_registration_form(self):
        print("\ntest_get_registration_form")
        response = self.client.get("/courses/register/test-course/")
        self.assertTemplateUsed(response, "register_course.html")
        self.assertEqual(response.status_code, 200)

        self.user_profile.delete()
        response = self.client.get("/courses/register/test-course/")
        self.assertRedirects(response, "/user/profile/", 302, 200)

        # Test messages: https://stackoverflow.com/a/46865530
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Please create a user profile and try again.",
            messages,
        )

    def test_user_is_registered_for_course(self):
        print("\ntest_user_is_registered_for_course")
        UserCourseRegistration.objects.create(
            user=self.user,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )
        # Test Redirect: https://stackoverflow.com/a/49353888
        response = self.client.get(f"/courses/register/{self.course.slug}/")
        self.assertRedirects(response, "/courses/", 302, 200)

    def test_post_valid_registration_form(self):
        print("\ntest_post_valid_registration_form")
        response = self.client.post(
            "/courses/register/test-course/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": False,
            },
        )
        self.assertRedirects(response, "/user/registrations/", 302, 200)
        queryset = UserCourseRegistration.objects.all()
        self.assertEqual(len(queryset), 1)

    def test_post_invalid_registration_form(self):
        print("\ntest_post_invalid_registration_form")
        response = self.client.post(f"/courses/register/{self.course.slug}/")
        self.assertEqual(response.status_code, 200)
        registrations = UserCourseRegistration.objects.all()
        self.assertEqual(len(registrations), 0)

    def test_auto_added_exam_grade(self):
        print("\ntest_auto_added_exam_grade")
        self.client.post(
            "/courses/register/test-course/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        registration = UserCourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertEqual(registration.exam_grade, self.user_profile.grade + 1)

    def test_invalid_exam_application(self):
        print("\ntest_invalid_exam_application")
        self.user_profile.grade = 6
        self.user_profile.save()
        response = self.client.post(
            "/courses/register/test-course/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        registration = UserCourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertFalse(registration.exam)

    def test_registration_fee_calculation_entire_course(self):
        print("\ntest_registration_fee_calculation_entire_course")
        self.client.post(
            "/courses/register/test-course/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        registration = UserCourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertEqual(
            registration.course.course_fee, registration.final_fee
        )

    def test_registration_fee_calculation_single_sessions(self):
        print("\ntest_registration_fee_calculation_single_sessions")
        self.another_session = CourseSession.objects.create(
            title="Another test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )

        self.client.post(
            "/courses/register/test-course/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        registration = UserCourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertEqual(self.session.session_fee, registration.final_fee)


class CancelUserCourseRegistrationTest(TestCase):
    """Tests for CancelCouresRegistration view"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(1),
            course_fee=50,
        )
        self.user = User.objects.create_user(
            username="test-user", password="testpassword"
        )
        self.client.force_login(self.user)
        self.registration = UserCourseRegistration.objects.create(
            user=self.user,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )
        self.user2 = User.objects.create_user(
            username="test-user2", password="testpassword"
        )
        self.registration2 = UserCourseRegistration.objects.create(
            user=self.user2,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )

    def test_cancel_valid_course_registration_post(self):
        print("\ntest_cancel_valid_course_registration_post")
        response = self.client.post(
            f"/user/registrations/cancel/{self.registration.pk}/"
        )
        self.assertRedirects(response, "/user/registrations/", 302, 200)
        registrations = UserCourseRegistration.objects.filter(
            pk=self.registration.pk
        )
        self.assertEqual(len(registrations), 0)

        # Test messages: https://stackoverflow.com/a/46865530
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            f"Your registration for {self.course.title} has been cancelled.",
            messages,
        )

    def test_cancel_forbidden_course_registration_post(self):
        print("\ntest_cancel_forbidden_course_registration_post")
        response = self.client.post(
            f"/user/registrations/cancel/{self.registration2.pk}/"
        )
        self.assertEqual(response.status_code, 403)

    def test_cancel_valid_course_registration_get(self):
        print("\ntest_cancel_valid_course_registration_get")
        response = self.client.get(
            f"/user/registrations/cancel/{self.registration.pk}/"
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Please cancel registrations by clicking the button from the "
            "My Registrations page.",
            messages,
        )

    def test_cancel_inexistent_course_registration_get(self):
        print("\ntest_get_cancel_inexistent_course_registration")
        response = self.client.get("/user/registrations/cancel/3/")
        self.assertEqual(response.status_code, 404)

    def test_cancel_forbidden_course_registration_get(self):
        print("\ntest_get_cancel_forbidden_course_registration")
        response = self.client.get(
            f"/user/registrations/cancel/{self.registration2.pk}/"
        )
        self.assertEqual(response.status_code, 403)


class UpdateUserCourseRegistrationTest(TestCase):
    """Tests for UpdateUserCourseRegistration view"""

    def setUp(self):
        self.course = Course.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(1),
            course_fee=50,
        )
        self.session = CourseSession.objects.create(
            title="Test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )
        self.user = User.objects.create_user(
            username="test-user", password="testpassword"
        )
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.create(user=self.user, grade=0)
        self.registration = UserCourseRegistration.objects.create(
            user=self.user,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )
        self.user2 = User.objects.create_user(
            username="test-user2", password="testpassword"
        )
        self.registration2 = UserCourseRegistration.objects.create(
            user=self.user2,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )

    def test_get_update_course_registration(self):
        print("\ntest_get_update_course_registration")
        response = self.client.get(
            f"/user/registrations/update/{self.registration.id}/"
        )
        self.assertTemplateUsed(response, "update_courseregistration.html")
        self.assertEqual(response.status_code, 200)

    def test_get_forbidden_update_course_registration(self):
        print("\ntest_get_forbidden_update_course_registration")
        response = self.client.get(
            f"/user/registrations/update/{self.registration2.id}/"
        )
        self.assertEqual(response.status_code, 403)

    def test_post_valid_update_course_registration(self):
        print("\ntest_post_valid_update_course_registration")
        response = self.client.post(
            f"/user/registrations/update/{self.registration.pk}/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        self.assertRedirects(response, "/user/registrations/", 302, 200)
        registration = UserCourseRegistration.objects.get(
            pk=self.registration.pk)
        self.assertEqual(registration.exam, True)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "You have successfully updated your registration for "
            f"{self.course.title}",
            messages,
        )

    def test_post_invalid_update_course_registration(self):
        print("\ntest_post_invalid_update_course_registration")
        response = self.client.post(
            f"/user/registrations/update/{self.registration.pk}/",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_courseregistration.html")
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Registration not submitted. "
            "Please select at least one session.",
            messages,
        )

    def test_post_forbidden_update_course_registration(self):
        print("\ntest_post_forbidden_update_course_registration")
        response = self.client.post(
            f"/user/registrations/update/{self.registration2.id}/"
        )
        self.assertEqual(response.status_code, 403)

    def test_update_registration_fee_calculation_entire_course(self):
        print("\ntest_registration_fee_calculation_entire_course")
        self.client.post(
            f"/user/registrations/update/{self.registration.pk}/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        self.registration.refresh_from_db()
        self.assertEqual(
            self.registration.course.course_fee, self.registration.final_fee
        )

    def test_update_registration_fee_calculation_single_sessions(self):
        print("\ntest_registration_fee_calculation_single_sessions")
        self.another_session = CourseSession.objects.create(
            title="Another test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )
        self.client.post(
            f"/user/registrations/update/{self.registration.pk}/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        self.registration.refresh_from_db()
        self.assertEqual(self.session.session_fee, self.registration.final_fee)

    def test_update_invalid_exam_application(self):
        print("\ntest_update_invalid_exam_application")
        self.user_profile.grade = 6
        self.user_profile.save()
        response = self.client.post(
            f"/user/registrations/update/{self.registration.pk}/",
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
            },
        )
        registration = UserCourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertFalse(registration.exam)
