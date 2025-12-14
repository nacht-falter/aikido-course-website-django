from datetime import date, time, timedelta

from django.test import TestCase

from courses.models import AccommodationOption, CourseSession, InternalCourse
from fees.models import Fee
from users.models import User, UserProfile

from .models import CourseRegistration


class TestCourseRegistrationFeeCalculation(TestCase):
    """Tests for CourseRegistration fee calculation logic"""

    def setUp(self):
        """Set up common test data"""
        # Create test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
            first_name="Test",
            last_name="User",
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user, dojo="Test Dojo", grade=3
        )

    def test_sensei_emmerson_dan_seminar_single_day(self):
        print("\ntest_sensei_emmerson_dan_seminar_single_day")
        # Create sensei_emmerson course with dan_seminar fee category
        course = InternalCourse.objects.create(
            title="Sensei Emmerson Dan Seminar",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
        )

        # Create sessions on same day
        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=course,
            date=date.today(),
            start_time=time(14, 0),
            end_time=time(16, 0),
        )

        # Create fee
        Fee.objects.create(
            course_type="sensei_emmerson",
            fee_category="dan_seminar",
            fee_type="single_day",
            amount=80.00,
        )

        # Create registration with single day selection
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Calculate fees
        selected_sessions = course.sessions.filter(id__in=[session1.id, session2.id])
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 80.00)

    def test_sensei_emmerson_entire_course_with_dan_prep(self):
        print("\ntest_sensei_emmerson_entire_course_with_dan_prep")
        course = InternalCourse.objects.create(
            title="Sensei Emmerson Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="sensei_emmerson",
            fee_category="regular",
            has_dan_preparation=True,
        )

        # Create sessions
        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="DAN Session",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_dan_preparation=True,
        )

        # Create fee
        Fee.objects.create(
            course_type="sensei_emmerson",
            fee_category="regular",
            fee_type="entire_course_dan_preparation",
            amount=150.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select all sessions
        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 150.00)

    def test_sensei_emmerson_entire_course_without_dan_prep(self):
        print("\ntest_sensei_emmerson_entire_course_without_dan_prep")
        course = InternalCourse.objects.create(
            title="Sensei Emmerson Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="sensei_emmerson",
            fee_category="regular",
            has_dan_preparation=True,
        )

        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="DAN Session",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_dan_preparation=True,
        )

        # Create fee for entire course without DAN prep
        Fee.objects.create(
            course_type="sensei_emmerson",
            fee_category="regular",
            fee_type="entire_course",
            amount=120.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select only non-DAN sessions
        selected_sessions = course.sessions.filter(is_dan_preparation=False)
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 120.00)

    def test_sensei_emmerson_single_session(self):
        print("\ntest_sensei_emmerson_single_session")
        course = InternalCourse.objects.create(
            title="Sensei Emmerson Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="sensei_emmerson",
            fee_category="regular",
        )

        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for single session
        Fee.objects.create(
            course_type="sensei_emmerson",
            fee_category="regular",
            fee_type="single_session",
            amount=40.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select only one session
        selected_sessions = course.sessions.filter(id=session1.id)
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 40.00)

    def test_hombu_dojo_single_day(self):
        print("\ntest_hombu_dojo_single_day")
        course = InternalCourse.objects.create(
            title="Hombu Dojo Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="hombu_dojo",
            fee_category="regular",
        )

        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for single day (hombu_dojo uses single_day fee_type when single_day=True)
        Fee.objects.create(
            course_type="hombu_dojo",
            fee_category="regular",
            fee_type="single_day",
            amount=100.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select only one session (single day)
        selected_sessions = course.sessions.filter(id=session1.id)
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 100.00)

    def test_hombu_dojo_entire_course(self):
        print("\ntest_hombu_dojo_entire_course")
        course = InternalCourse.objects.create(
            title="Hombu Dojo Entire Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="hombu_dojo",
            fee_category="regular",
        )

        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for entire course
        Fee.objects.create(
            course_type="hombu_dojo",
            fee_category="regular",
            fee_type="entire_course",
            amount=150.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select all sessions (entire course)
        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 150.00)

    def test_external_teacher_dan_seminar(self):
        print("\ntest_external_teacher_dan_seminar")
        course = InternalCourse.objects.create(
            title="External Teacher Dan Seminar",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="dan_seminar",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for single session
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="dan_seminar",
            fee_type="single_session",
            amount=30.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 30.00)

    def test_external_teacher_entire_course_without_dan_prep(self):
        print("\ntest_external_teacher_entire_course_without_dan_prep")
        course = InternalCourse.objects.create(
            title="External Teacher Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="external_teacher",
            fee_category="regular",
            has_dan_preparation=True,
        )

        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="DAN Session",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_dan_preparation=True,
        )

        # Create fee for entire course without DAN prep
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=120.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select only non-DAN sessions (entire course without DAN prep)
        selected_sessions = course.sessions.filter(is_dan_preparation=False)
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 120.00)

    def test_external_teacher_single_session(self):
        print("\ntest_external_teacher_single_session")
        course = InternalCourse.objects.create(
            title="External Teacher Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="external_teacher",
            fee_category="regular",
        )

        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for single session
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="single_session",
            amount=35.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select only one session
        selected_sessions = course.sessions.filter(id=session1.id)
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 35.00)

    def test_dan_bw_teacher_single_session(self):
        print("\ntest_dan_bw_teacher_single_session")
        course = InternalCourse.objects.create(
            title="DAN BW Teacher Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="dan_bw_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for single session
        Fee.objects.create(
            course_type="dan_bw_teacher",
            fee_category="regular",
            fee_type="single_session",
            amount=25.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 25.00)

    def test_children_entire_course(self):
        print("\ntest_children_entire_course")
        course = InternalCourse.objects.create(
            title="Children Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="children",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for entire course
        Fee.objects.create(
            course_type="children",
            fee_category="regular",
            fee_type="entire_course",
            amount=25.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 25.00)

    def test_family_reunion_entire_course_with_dan(self):
        print("\ntest_family_reunion_entire_course_with_dan")
        course = InternalCourse.objects.create(
            title="Family Reunion",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="family_reunion",
            fee_category="family_reunion",
        )

        # Create sessions on different days
        session1 = CourseSession.objects.create(
            title="Session Day 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="DAN Session Day 2",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_dan_preparation=True,
        )

        # Create fee
        Fee.objects.create(
            course_type="family_reunion",
            fee_category="family_reunion",
            fee_type="entire_course_with_dan_seminar",
            amount=200.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select all sessions (covering all days)
        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 200.00)

    def test_family_reunion_single_day_with_dan(self):
        print("\ntest_family_reunion_single_day_with_dan")
        course = InternalCourse.objects.create(
            title="Family Reunion",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=2),
            course_type="family_reunion",
            fee_category="family_reunion",
        )

        # Create sessions on different days
        session1 = CourseSession.objects.create(
            title="Session Day 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="DAN Session Day 2",
            course=course,
            date=date.today() + timedelta(days=1),
            start_time=time(10, 0),
            end_time=time(12, 0),
            is_dan_preparation=True,
        )
        session3 = CourseSession.objects.create(
            title="Session Day 3",
            course=course,
            date=date.today() + timedelta(days=2),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee for single day with DAN
        Fee.objects.create(
            course_type="family_reunion",
            fee_category="family_reunion",
            fee_type="single_day_with_dan_seminar",
            amount=80.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        # Select only DAN session (one day)
        selected_sessions = course.sessions.filter(id=session2.id)
        final_fee = registration.calculate_fees(course, selected_sessions)

        self.assertEqual(final_fee, 80.00)

    def test_accommodation_fee_addition(self):
        print("\ntest_accommodation_fee_addition")
        course = InternalCourse.objects.create(
            title="Course with Accommodation",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create accommodation option
        accommodation = AccommodationOption.objects.create(
            course=course, name="2 Nights", fee=50.00
        )

        # Create course fee (entire course since all sessions selected)
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=30.00,
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
            accommodation_option=accommodation,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Should be course fee (30) + accommodation (50) = 80
        self.assertEqual(final_fee, 80.00)

    def test_cash_payment_extra_fee(self):
        print("\ntest_cash_payment_extra_fee")
        course = InternalCourse.objects.create(
            title="Cash Payment Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee with cash extra
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
            extra_fee_cash=5.00,
        )

        # Registration with cash payment (payment_method=1)
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=1,  # Cash
            dan_member=True,  # To avoid external fee
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Should be base (100) + cash extra (5) = 105
        self.assertEqual(final_fee, 105.00)

    def test_non_dan_member_external_fee(self):
        print("\ntest_non_dan_member_external_fee")
        course = InternalCourse.objects.create(
            title="External Fee Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee with external extra
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
            extra_fee_external=10.00,
        )

        # Registration with non-DAN-member (dan_member=False)
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,  # Bank to avoid cash fee
            dan_member=False,  # Not a DAN member
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Should be base (100) + external (10) = 110
        self.assertEqual(final_fee, 110.00)

    def test_dan_member_no_external_fee(self):
        print("\ntest_dan_member_no_external_fee")
        course = InternalCourse.objects.create(
            title="DAN Member Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee with external extra
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
            extra_fee_external=10.00,
        )

        # Registration with DAN member (dan_member=True)
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=True,  # Is a DAN member
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Should be base (100) only, no external fee
        self.assertEqual(final_fee, 100.00)

    def test_cash_and_non_dan_member_combined(self):
        print("\ntest_cash_and_non_dan_member_combined")
        course = InternalCourse.objects.create(
            title="Combined Extras Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee with both extras
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
            extra_fee_cash=5.00,
            extra_fee_external=10.00,
        )

        # Registration with both cash and non-DAN-member
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=1,  # Cash
            dan_member=False,  # Not a DAN member
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Should be base (100) + cash (5) + external (10) = 115
        self.assertEqual(final_fee, 115.00)

    def test_discount_application(self):
        print("\ntest_discount_application")
        course = InternalCourse.objects.create(
            title="Discount Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
            discount_percentage=20,  # 20% discount
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
        )

        # Registration with discount=True
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=True,
            accept_terms=True,
            discount=True,  # Apply discount
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Should be base (100) * 0.8 = 80
        self.assertEqual(final_fee, 80.00)

    def test_discount_with_extras(self):
        print("\ntest_discount_with_extras")
        course = InternalCourse.objects.create(
            title="Discount with Extras Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
            discount_percentage=20,  # 20% discount
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create fee with extras
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
            extra_fee_cash=5.00,
            extra_fee_external=10.00,
        )

        # Registration with discount and extras
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=1,  # Cash
            dan_member=False,  # Not DAN member
            accept_terms=True,
            discount=True,  # Apply discount
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Discount applies to total including extras: (100 + 5 + 10) * 0.8 = 92
        self.assertEqual(final_fee, 92.00)

    def test_accommodation_not_discounted(self):
        print("\ntest_accommodation_not_discounted")
        course = InternalCourse.objects.create(
            title="Accommodation Discount Course",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="external_teacher",
            fee_category="regular",
            discount_percentage=20,  # 20% discount
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        # Create accommodation option
        accommodation = AccommodationOption.objects.create(
            course=course, name="2 Nights", fee=50.00
        )

        # Create fee
        Fee.objects.create(
            course_type="external_teacher",
            fee_category="regular",
            fee_type="entire_course",
            amount=100.00,
        )

        # Registration with discount and accommodation
        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=True,
            accept_terms=True,
            discount=True,  # Apply discount
            accommodation_option=accommodation,
        )

        selected_sessions = course.sessions.all()
        final_fee = registration.calculate_fees(course, selected_sessions)

        # Discount on course fee only: (100 * 0.8) + 50 = 130
        # Accommodation is NOT discounted
        self.assertEqual(final_fee, 130.00)


class TestCourseRegistrationErrorHandling(TestCase):
    """Tests for fee calculation error handling"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )
        self.user_profile = UserProfile.objects.create(user=self.user, dojo="Test Dojo")

    def test_calculate_fees_raises_error_when_fee_not_found_single_session(self):
        print("\ntest_calculate_fees_raises_error_when_fee_not_found_single_session")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()

        # Should raise ValueError because no fee exists
        with self.assertRaises(ValueError):
            registration.calculate_fees(course, selected_sessions)

    def test_calculate_fees_raises_error_when_fee_not_found_family_reunion(self):
        print("\ntest_calculate_fees_raises_error_when_fee_not_found_family_reunion")
        course = InternalCourse.objects.create(
            title="Family Reunion",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=1),
            course_type="family_reunion",
            fee_category="family_reunion",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        selected_sessions = course.sessions.filter(id=session.id)

        # Should raise ValueError because no fee exists
        with self.assertRaises(ValueError):
            registration.calculate_fees(course, selected_sessions)

    def test_calculate_fees_raises_error_when_fee_not_found_entire_course(self):
        print("\ntest_calculate_fees_raises_error_when_fee_not_found_entire_course")
        course = InternalCourse.objects.create(
            title="Children Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="children",
            fee_category="regular",
        )

        session = CourseSession.objects.create(
            title="Session",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            dan_member=False,
            accept_terms=True,
        )

        selected_sessions = course.sessions.all()

        # Should raise ValueError because no fee exists
        with self.assertRaises(ValueError):
            registration.calculate_fees(course, selected_sessions)


class TestCourseRegistrationGuestUser(TestCase):
    """Tests for guest user registration"""

    def test_set_exam_for_guest_user(self):
        print("\ntest_set_exam_for_guest_user")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        # Create guest registration (no user)
        registration = CourseRegistration.objects.create(
            course=course,
            first_name="Guest",
            last_name="User",
            email="guest@example.com",
            grade=3,  # Less than 6
            exam=True,
            payment_method=0,
            accept_terms=True,
        )

        # Call set_exam
        registration.set_exam()

        # Should set exam_grade to grade + 1
        self.assertEqual(registration.exam_grade, 4)

    def test_set_exam_for_guest_user_max_grade(self):
        print("\ntest_set_exam_for_guest_user_max_grade")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        # Create guest registration with grade >= 6
        registration = CourseRegistration.objects.create(
            course=course,
            first_name="Guest",
            last_name="User",
            email="guest@example.com",
            grade=6,  # Max grade
            exam=True,
            payment_method=0,
            accept_terms=True,
        )

        # Call set_exam
        registration.set_exam()

        # Should set exam to False
        self.assertFalse(registration.exam)

    def test_set_exam_for_registered_user(self):
        print("\ntest_set_exam_for_registered_user")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        # Create user with grade < 6
        user = User.objects.create_user(
            username="examuser",
            password="testpassword",
            email="exam@example.com",
        )
        user_profile = UserProfile.objects.create(user=user, dojo="Test Dojo", grade=4)

        # Create registration for user
        registration = CourseRegistration.objects.create(
            user=user,
            course=course,
            exam=True,
            payment_method=0,
            accept_terms=True,
        )

        # Call set_exam with user parameter
        registration.set_exam(user=user)

        # Should set exam_grade to user's grade + 1
        self.assertEqual(registration.exam_grade, 5)

    def test_set_exam_for_registered_user_max_grade(self):
        print("\ntest_set_exam_for_registered_user_max_grade")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        # Create user with grade >= 6
        user = User.objects.create_user(
            username="maxgradeuser",
            password="testpassword",
            email="maxgrade@example.com",
        )
        user_profile = UserProfile.objects.create(user=user, dojo="Test Dojo", grade=6)

        # Create registration for user
        registration = CourseRegistration.objects.create(
            user=user,
            course=course,
            exam=True,
            payment_method=0,
            accept_terms=True,
        )

        # Call set_exam with user parameter
        registration.set_exam(user=user)

        # Should set exam to False (can't exam beyond grade 6)
        self.assertFalse(registration.exam)


class TestCourseRegistrationDisplayMethods(TestCase):
    """Tests for display methods"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="test@example.com",
        )
        self.user_profile = UserProfile.objects.create(user=self.user, dojo="Test Dojo")

    def test_truncated_session_display_entire_course(self):
        print("\ntest_truncated_session_display_entire_course")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        session1 = CourseSession.objects.create(
            title="Session 1",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=course,
            date=date.today(),
            start_time=time(14, 0),
            end_time=time(16, 0),
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            accept_terms=True,
        )
        registration.selected_sessions.add(session1, session2)

        display = registration.truncated_session_display()
        # Check for German translation "Ganzer Lehrgang" (Entire Course)
        self.assertIn("Ganzer Lehrgang", display)

    def test_truncated_session_display_truncated(self):
        print("\ntest_truncated_session_display_truncated")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        session1 = CourseSession.objects.create(
            title="Very Long Session Title That Will Definitely Be Truncated",
            course=course,
            date=date.today(),
            start_time=time(10, 0),
            end_time=time(12, 0),
        )
        session2 = CourseSession.objects.create(
            title="Session 2",
            course=course,
            date=date.today(),
            start_time=time(14, 0),
            end_time=time(16, 0),
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            accept_terms=True,
        )
        # Only select one session
        registration.selected_sessions.add(session1)

        display = registration.truncated_session_display()
        # Should be truncated and contain "..."
        self.assertIn("...", display)

    def test_truncated_comment(self):
        print("\ntest_truncated_comment")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            accept_terms=True,
            comment="This is a very long comment that should be truncated at 30 characters",
        )

        display = registration.truncated_comment()
        self.assertIn("...", display)

    def test_truncated_comment_short(self):
        print("\ntest_truncated_comment_short")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            accept_terms=True,
            comment="Short comment",
        )

        display = registration.truncated_comment()
        self.assertNotIn("...", display)
        self.assertIn("Short comment", display)

    def test_truncated_comment_empty(self):
        print("\ntest_truncated_comment_empty")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            accept_terms=True,
            comment="",  # Empty comment
        )

        display = registration.truncated_comment()
        self.assertEqual(display, "")

    def test_str_method(self):
        print("\ntest_str_method")
        course = InternalCourse.objects.create(
            title="Course",
            start_date=date.today(),
            end_date=date.today(),
            course_type="external_teacher",
            fee_category="regular",
        )

        registration = CourseRegistration.objects.create(
            user=self.user,
            course=course,
            payment_method=0,
            accept_terms=True,
        )

        # __str__ should return "first_name last_name"
        # The save method populates first_name and last_name from the user
        self.assertEqual(str(registration), f"{self.user.first_name} {self.user.last_name}")
