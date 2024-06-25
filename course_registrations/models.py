from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from courses.models import CourseSession, InternalCourse
from danbw_website import constants
from users.models import User, UserProfile


class UserCourseRegistration(models.Model):
    """Represents a registration for a course by a user"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registrations", verbose_name=_("User")
    )
    course = models.ForeignKey(
        InternalCourse, on_delete=models.CASCADE, verbose_name=_("Course"))
    selected_sessions = models.ManyToManyField(
        CourseSession, verbose_name=_("Selected sessions"), blank=False)
    registration_date = models.DateTimeField(
        _("Registration date"),  auto_now_add=True)
    exam = models.BooleanField(_("Exam"), default=False)
    exam_grade = models.IntegerField(
        _("Exam Grade"),  choices=constants.EXAM_GRADE_CHOICES, default=constants.RED_BELT)
    exam_passed = models.BooleanField(_("Exam passed"), null=True)
    grade_updated = models.BooleanField(_("Grade updated"),  default=False)
    accept_terms = models.BooleanField(_("Accept terms"),  default=False)
    discount = models.BooleanField(_("Discount"), default=False)
    final_fee = models.IntegerField(_("Final fee"), default=0)
    payment_status = models.IntegerField(
        _("Payment status"), choices=constants.PAYMENT_STATUS, default=0)
    payment_method = models.IntegerField(
        _("Payment method"), choices=constants.PAYMENT_METHODS, default=0)
    comment = models.TextField(_("Comment"), blank=True)
    dinner = models.BooleanField(_("Dinner"),  blank=True, null=True)
    overnight_stay = models.BooleanField(
        _("Overnight stay"),  blank=True, null=True)

    class Meta:
        # Set unique constraint: https://docs.djangoproject.com/en/4.2/
        # ref/models/constraints/#django.db.models.UniqueConstraint
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_registration"
            )
        ]
        verbose_name = _("Course Registration (User)")
        verbose_name_plural = _("Course Registrations (User)")

    def calculate_fees(self, course, selected_sessions):
        final_fee = 0
        if len(selected_sessions) == len(course.sessions.all()):
            final_fee = course.course_fee if self.payment_method == 0 else course.course_fee_cash
        else:
            for session in selected_sessions:
                final_fee += session.session_fee if self.payment_method == 0 else session.session_fee_cash
        return final_fee * course.discount_percentage / 100 if self.discount else final_fee

    def set_exam(self, user):
        if self.exam:
            user_profile = get_object_or_404(UserProfile, user=user)
            if user_profile.grade < 6:
                self.exam_grade = user_profile.grade + 1
            else:
                self.exam = False

    def save(self, *args, **kwargs):
        if not self.course.course_type == "international":
            self.dinner = 0
            self.overnight_stay = 0

        super().save(*args, **kwargs)


class GuestCourseRegistration(models.Model):
    """Represents a registration for a course by a guest"""

    email = models.EmailField(_("Email"))
    first_name = models.CharField(_("First name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    course = models.ForeignKey(
        InternalCourse, on_delete=models.CASCADE, verbose_name=_("Course"))
    selected_sessions = models.ManyToManyField(
        CourseSession, blank=False, verbose_name=_("Selected sessions"))
    registration_date = models.DateTimeField(
        _("Registration date"), auto_now_add=True)
    dojo = models.CharField(_("Dojo"), max_length=5,
                            choices=constants.DOJO_CHOICES, blank=False)
    other_dojo = models.CharField(_("Other dojo"), max_length=100, blank=True)
    grade = models.IntegerField(
        _("Grade"), choices=constants.GRADE_CHOICES, default=constants.RED_BELT, blank=False)
    exam = models.BooleanField(_("Exam"), default=False)
    exam_grade = models.IntegerField(
        _("Exam Grade"), choices=constants.EXAM_GRADE_CHOICES, blank=True, null=True)
    accept_terms = models.BooleanField(_("Accept terms"), default=False)
    discount = models.BooleanField(_("Discount"), default=False)
    final_fee = models.IntegerField(_("Final Fee"), default=0)
    payment_status = models.IntegerField(
        _("Payment status"), choices=constants.PAYMENT_STATUS, default=0)
    payment_method = models.IntegerField(
        _("Payment method"), choices=constants.PAYMENT_METHODS, default=0)
    comment = models.TextField(_("Comment"), blank=True)
    dinner = models.BooleanField(_("Dinner"), blank=True, null=True)
    overnight_stay = models.BooleanField(
        _("Overnight stay"), blank=True, null=True)

    class Meta:
        # Set unique constraint: https://docs.djangoproject.com/en/4.2/
        # ref/models/constraints/#django.db.models.UniqueConstraint
        constraints = [
            models.UniqueConstraint(
                fields=["email", "course"],
                name="unique_guest_registration"
            )
        ]
        verbose_name = _("Course Registration (Guest)")
        verbose_name_plural = _("Guest Course Registrations (Guest)")

    def calculate_fees(self, course, selected_sessions):
        final_fee = 0
        if len(selected_sessions) == len(course.sessions.all()):
            final_fee = course.course_fee if self.payment_method == 0 else course.course_fee_cash
        else:
            for session in selected_sessions:
                final_fee += session.session_fee if self.payment_method == 0 else session.session_fee_cash
        return final_fee * course.discount_percentage / 100 if self.discount else final_fee

    def set_exam(self):
        if self.exam:
            if self.grade < 6:
                self.exam_grade = self.grade + 1
            else:
                self.exam = False

    def save(self, *args, **kwargs):
        if not self.course.course_type == "international":
            self.dinner = 0
            self.overnight_stay = 0

        if self.dojo == "other":
            self.dojo = self.other_dojo
        super().save(*args, **kwargs)
