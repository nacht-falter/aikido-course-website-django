from datetime import date, datetime, timedelta

from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from courses.models import Course, CourseSession, InternalCourse
from fees.models import Fee
from users.models import User, UserProfile

from .models import CourseRegistration


class RegisterCourseTest(TestCase):
    """Tests for RegisterCourse view"""

    def setUp(self):
        self.course = InternalCourse.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(1),
            course_type="external_teacher",
            fee_category="dan_member",
            description="Test description",
            discount_percentage=0,
        )
        self.fee = Fee.objects.create(
            course_type="external_teacher",
            fee_category="dan_member",
            fee_type="entire_course",
            amount=50,
        )
        self.fee = Fee.objects.create(
            course_type="external_teacher",
            fee_category="dan_member",
            fee_type="single_session",
            amount=20,
        )
        self.session = CourseSession.objects.create(
            title="Test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )
        self.session2 = CourseSession.objects.create(
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
            username="test-user", password="testpassword", email="test@example.com", first_name="Test", last_name="User"
        )
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.create(user=self.user, dojo="AAR")

    def test_get_registration_form(self):
        print("\ntest_get_registration_form")
        url = reverse("register_course", kwargs={"slug": self.course.slug})
        response = self.client.get(url)
        self.assertTemplateUsed(response, "register_course.html")
        self.assertEqual(response.status_code, 200)

        self.user_profile.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("userprofile")))

        # Test messages: https://stackoverflow.com/a/46865530
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Bitte erstelle ein Benutzerprofil, um fortzufahren.",
            messages,
        )

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
        url = reverse("register_course", kwargs={"slug": self.course.slug})
        response = self.client.get(url)
        self.assertRedirects(response, reverse("course_list"), 302, 200)

    def test_post_valid_registration_form(self):
        print("\ntest_post_valid_registration_form")
        url = reverse("register_course", kwargs={"slug": self.course.slug})
        response = self.client.post(
            url,
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": False,
                "payment_method": 0,
            },
        )
        self.assertRedirects(response, reverse("courseregistration_list"), 302, 200)
        queryset = CourseRegistration.objects.all()
        self.assertEqual(len(queryset), 1)

    def test_post_invalid_registration_form(self):
        print("\ntest_post_invalid_registration_form")
        url = reverse("register_course", kwargs={"slug": self.course.slug})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        registrations = CourseRegistration.objects.all()
        self.assertEqual(len(registrations), 0)

    def test_auto_added_exam_grade(self):
        print("\ntest_auto_added_exam_grade")
        url = reverse("register_course", kwargs={"slug": self.course.slug})
        self.client.post(
            url,
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
                "payment_method": 0,
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
            reverse("register_course", kwargs={"slug": "test-course"}),
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
                "payment_method": 0,
            },
        )
        registration = CourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        self.assertFalse(registration.exam)

    def test_registration_fee_calculation_entire_course(self):
        print("\ntest_registration_fee_calculation_entire_course")
        response = self.client.post(
            reverse("register_course", kwargs={"slug": "test-course"}),
            {
                "selected_sessions": [self.session.id, self.session2.id],
                "accept_terms": True,
                "exam": True,
                "payment_method": 0,
            },
        )
        registration = CourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        expected_fee = Fee.get_fee(
            self.course.course_type,
            self.course.fee_category,
            "entire_course",
            registration.payment_method,
            registration.dan_member,
        )
        self.assertEqual(
            expected_fee, registration.final_fee
        )

    def test_registration_fee_calculation_single_sessions(self):
        print("\ntest_registration_fee_calculation_single_sessions")
        self.single_session_fee = Fee.objects.get(
            course_type="external_teacher",
            fee_category="dan_member",
            fee_type="single_session",
            amount=20,
        )
        self.another_session = CourseSession.objects.create(
            title="Another test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )

        self.client.post(
            reverse("register_course", kwargs={"slug": "test-course"}),
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
                "payment_method": 0,
            },
        )
        registration = CourseRegistration.objects.get(
            course=self.course,
            user=self.user,
        )
        expected_fee = Fee.get_fee(
            self.course.course_type,
            self.course.fee_category,
            "single_session",
            registration.payment_method,
            registration.dan_member,
        )
        self.assertEqual(expected_fee, registration.final_fee)


class CancelUserCourseRegistrationTest(TestCase):
    """Tests for CancelCouresRegistration view"""

    def setUp(self):
        self.course = InternalCourse.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(1),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
            description="Test description",
            discount_percentage=0,
        )
        self.user = User.objects.create_user(
            username="test-user", password="testpassword", email="test@example.com", first_name="Test", last_name="User"
        )
        self.client.force_login(self.user)
        self.user_profile = UserProfile.objects.create(user=self.user, dojo="AAR")
        self.registration = CourseRegistration.objects.create(
            user=self.user,
            course=self.course,
            payment_status=0,
            accept_terms=True,
            exam=False,
            comment="Test comment",
        )
        self.user2 = User.objects.create_user(
            username="test-user2", password="testpassword", email="test2@example.com", first_name="Test", last_name="User2"
        )
        self.user_profile2 = UserProfile.objects.create(user=self.user2)
        self.registration2 = CourseRegistration.objects.create(
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
            reverse("cancel_courseregistration", kwargs={"pk": self.registration.pk})
        )
        self.assertRedirects(response, reverse("courseregistration_list"), 302, 200)
        registrations = CourseRegistration.objects.filter(
            pk=self.registration.pk
        )
        self.assertEqual(len(registrations), 0)

        # Test messages: https://stackoverflow.com/a/46865530
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            f"Deine Anmeldung für {self.course.title} wurde storniert.",
            messages,
        )

    def test_cancel_forbidden_course_registration_post(self):
        print("\ntest_cancel_forbidden_course_registration_post")
        response = self.client.post(
            reverse("cancel_courseregistration", kwargs={"pk": self.registration2.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_cancel_valid_course_registration_get(self):
        print("\ntest_cancel_valid_course_registration_get")
        response = self.client.get(
            reverse("cancel_courseregistration", kwargs={"pk": self.registration.pk})
        )
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Bitte storniere Anmeldungen durch Klicken auf den Button auf "
            "der Seite 'Meine Anmeldungen'.",
            messages,
        )

    def test_cancel_inexistent_course_registration_get(self):
        print("\ntest_cancel_inexistent_course_registration_get")
        response = self.client.get(reverse("cancel_courseregistration", kwargs={"pk": 3}))
        self.assertEqual(response.status_code, 404)

    def test_cancel_forbidden_course_registration_get(self):
        print("\ntest_get_cancel_forbidden_course_registration")
        response = self.client.get(
            reverse("cancel_courseregistration", kwargs={"pk": self.registration2.pk})
        )
        self.assertEqual(response.status_code, 403)


class UpdateUserCourseRegistrationTest(TestCase):
    """Tests for UpdateUserCourseRegistration view"""

    def setUp(self):
        self.course = InternalCourse.objects.create(
            title="Test course",
            slug="test-course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            registration_status=(1),
            course_type="dan_bw_teacher",
            fee_category="dan_member",
            description="Test description",
            discount_percentage=0,
        )
        self.fee = Fee.objects.create(
            course_type="dan_bw_teacher",
            fee_category="dan_member",
            fee_type="entire_course",
            amount=50,
        )
        self.fee_single = Fee.objects.create(
            course_type="dan_bw_teacher",
            fee_category="dan_member",
            fee_type="single_session",
            amount=50,
        )
        self.session = CourseSession.objects.create(
            title="Test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )
        self.user = User.objects.create_user(
            username="test-user", password="testpassword", email="test@example.com", first_name="Test", last_name="User"
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
        self.user2 = User.objects.create_user(
            username="test-user2", password="testpassword", email="test2@example.com", first_name="Test", last_name="User2"
        )
        self.user_profile2 = UserProfile.objects.create(user=self.user2, grade=0)
        self.registration2 = CourseRegistration.objects.create(
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
            reverse("update_courseregistration", kwargs={"pk": self.registration.id})
        )
        self.assertTemplateUsed(response, "update_courseregistration.html")
        self.assertEqual(response.status_code, 200)

    def test_get_forbidden_update_course_registration(self):
        print("\ntest_get_forbidden_update_course_registration")
        response = self.client.get(
            reverse("update_courseregistration", kwargs={"pk": self.registration2.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_post_valid_update_course_registration(self):
        print("\ntest_post_valid_update_course_registration")
        response = self.client.post(
            reverse("update_courseregistration", kwargs={"pk": self.registration.pk}),
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
                "payment_method": 0
            },
        )
        self.assertRedirects(response, reverse("courseregistration_list"), 302, 200)
        registration = CourseRegistration.objects.get(
            pk=self.registration.pk)
        self.assertEqual(registration.exam, True)

        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Du hast Deine Anmeldung erfolgreich aktualisiert für "
            f"{self.course.title}",
            messages,
        )

    def test_post_invalid_update_course_registration(self):
        print("\ntest_post_invalid_update_course_registration")
        response = self.client.post(
            reverse("update_courseregistration", kwargs={"pk": self.registration.pk}),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "update_courseregistration.html")
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn(
            "Anmeldung nicht übermittelt. Bitte wähle mindestens eine Einheit aus.",
            messages,
        )

    def test_post_forbidden_update_course_registration(self):
        print("\ntest_post_forbidden_update_course_registration")
        response = self.client.post(
            reverse("update_courseregistration", kwargs={"pk": self.registration2.id})
        )
        self.assertEqual(response.status_code, 403)

    def test_update_registration_fee_calculation_entire_course(self):
        print("\ntest_registration_fee_calculation_entire_course")
        response = self.client.post(
            reverse("update_courseregistration", kwargs={"pk": self.registration.pk}),
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
                "payment_method": 0,
            },
        )
        self.registration.refresh_from_db()
        expected_fee = Fee.get_fee(
            self.course.course_type,
            self.course.fee_category,
            "entire_course",
            self.registration.payment_method,
            self.registration.dan_member,
        )
        self.assertEqual(
            expected_fee, self.registration.final_fee
        )

    def test_update_registration_fee_calculation_single_sessions(self):
        print("\ntest_update_registration_fee_calculation_single_sessions")
        self.another_session = CourseSession.objects.create(
            title="Another test session",
            course=self.course,
            date=date.today(),
            start_time=datetime.now().time(),
            end_time=datetime.now().time(),
        )
        response = self.client.post(
            reverse("update_courseregistration", kwargs={"pk": self.registration.pk}),
            {
                "selected_sessions": [self.session.id],
                "accept_terms": True,
                "exam": True,
                "payment_method": 0,
            },
        )
        self.registration.refresh_from_db()
        expected_fee = Fee.get_fee(
            self.course.course_type,
            self.course.fee_category,
            "single_session",
            self.registration.payment_method,
            self.registration.dan_member,
        )
        self.assertEqual(expected_fee, self.registration.final_fee)

    def test_update_invalid_exam_application(self):
        print("\ntest_update_invalid_exam_application")
        self.user_profile.grade = 6
        self.user_profile.save()
        response = self.client.post(
            reverse("update_courseregistration", kwargs={"pk": self.registration.pk}),
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
