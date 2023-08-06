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

    def test_user_is_registered_for_course(self):
        print("\ntest_user_is_registered_for_course")
        CourseRegistration.objects.create(
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
        queryset = CourseRegistration.objects.all()
        self.assertEqual(len(queryset), 1)

    def test_post_invalid_registration_form(self):
        print("\ntest_post_invalid_registration_form")
        response = self.client.post(f"/courses/register/{self.course.slug}/")
        self.assertEqual(response.status_code, 200)
        registrations = CourseRegistration.objects.all()
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
        registration = CourseRegistration.objects.get(
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
        registration = CourseRegistration.objects.get(
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
        registration = CourseRegistration.objects.get(
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
        registration = CourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertEqual(self.session.session_fee, registration.final_fee)


class CancelCourseRegistrationTest(TestCase):
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
        self.registration = CourseRegistration.objects.create(
            user=self.user,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )

    def test_cancel_course_registration(self):
        print("\ntest_cancel_course_registration")
        response = self.client.post(
            f"/user/registrations/cancel/{self.registration.pk}/"
        )
        self.assertRedirects(response, "/user/registrations/", 302, 200)
        registrations = CourseRegistration.objects.filter(
            pk=self.registration.pk
        )
        self.assertEqual(len(registrations), 0)

        # Test messages: https://stackoverflow.com/a/46865530
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            f"Your registration for {self.course.title} has been cancelled.",
            messages,
        )


class UpdateCourseRegistrationTest(TestCase):
    """Tests for UpdateCourseRegistration view"""

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
        self.registration = CourseRegistration.objects.create(
            user=self.user,
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
        registration = CourseRegistration.objects.get(pk=self.registration.pk)
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
        registration = CourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertFalse(registration.exam)


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


class ContactPageTest(TestCase):
    """Tests for Contact Page view"""

    def test_get_contact_page(self):
        print("\ntest_get_contact_page")
        response = self.client.get("/contact/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("contact.html")

    def test_post_valid_contact_form(self):
        print("\ntest_post_valid_contact_form")
        form_data = {
            "subject": "Test Subject",
            "message": "Test message",
            "from_email": "from@example.com",
        }
        response = self.client.post("/contact/", form_data)
        self.assertRedirects(response, "/", 302, 200)

        # Test email documentation: https://docs.djangoproject.com/en/
        # 4.2/topics/testing/tools/#email-services
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Test Subject")

    def test_post_invalid_contact_form(self):
        print("\ntest_post_invalid_contact_form")
        response = self.client.post("/contact/")
        self.assertEqual(response.status_code, 200)

    def test_bad_header_error(self):
        print("\ntest_post_invalid_contact_form")

        # Test bad header: https://stackoverflow.com/a/27268861
        form_data = {
            "subject": "Test\nSubject",
            "message": "Test message",
            "from_email": "from@example.com",
        }
        response = self.client.post("/contact/", form_data)
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Invalid Header found. Please try again.",
            messages,
        )


class PageTest(TestCase):
    """Tests for PageList and PageDetail views"""

    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
            slug="test-category",
        )
        self.page = Page.objects.create(
            title="Test page",
            slug="test-page",
            category=self.category,
            status=1,
            content="Test Content",
        )

    def test_get_page_list(self):
        print("\ntest_get_page_list")
        response = self.client.get(
            f"/pages/{self.category.slug}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context["object_list"], Page.objects.all()
        )

    def test_get_page(self):
        print("\ntest_get_page")
        response = self.client.get(
            f"/pages/{self.category.slug}/{self.page.slug}/"
        )
        self.assertEqual(response.status_code, 200)
