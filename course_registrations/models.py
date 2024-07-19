from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from courses.models import CourseSession, InternalCourse
from danbw_website import constants
from users.models import User, UserProfile


class CourseRegistration(models.Model):
    """Represents a registration for a course by a user or guest"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="registrations",
        verbose_name=_("Participant"),
        help_text=_("The user who is registering for the course."),
        null=True,
        blank=True
    )
    email = models.EmailField(
        _("Email"),
        help_text=_("The email address of the participant."),
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=100,
        help_text=_("The first name of the participant."),
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=100,
        help_text=_("The last name of the participant."),
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        InternalCourse,
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
        help_text=_("The course for which the participant is registering.")
    )
    selected_sessions = models.ManyToManyField(
        CourseSession,
        blank=False,
        verbose_name=_("Selected sessions"),
        help_text=_(
            "The sessions within the course that the participant has selected.")
    )
    registration_date = models.DateTimeField(
        _("Registration date"),
        auto_now_add=True,
        help_text=_(
            "The date and time when the participant registered for the course.")
    )
    dojo = models.CharField(
        _("Dojo"),
        max_length=5,
        choices=constants.DOJO_CHOICES,
        blank=True,
        null=True,
        help_text=_("The dojo the participant belongs to.")
    )
    other_dojo = models.CharField(
        _("Other Dojo"),
        max_length=100,
        blank=True,
        help_text=_("The name of the participant's Dojo outside of D.A.N. BW.")
    )
    grade = models.IntegerField(
        _("Grade"),
        choices=constants.GRADE_CHOICES,
        default=constants.RED_BELT,
        blank=True,
        null=True,
        help_text=_("The grade of the participant.")
    )
    exam = models.BooleanField(
        _("Exam"),
        default=False,
        help_text=_(
            "Indicates whether the participant would like to take an exam.")
    )
    exam_grade = models.IntegerField(
        _("Exam Grade"),
        choices=constants.EXAM_GRADE_CHOICES,
        blank=True,
        null=True,
        help_text=_("The grade of the exam the participant would like to take.")
    )
    exam_passed = models.BooleanField(
        _("Exam Passed"),
        null=True,
    )
    grade_updated = models.BooleanField(
        _("Grade Updated"),
        default=False,
    )
    accept_terms = models.BooleanField(
        _("Accept terms"),
        default=False,
        help_text=_(
            "Indicates whether the participant has accepted the terms and conditions.")
    )
    discount = models.BooleanField(
        _("Discount"),
        default=False,
        help_text=_(
            "Indicates whether the participant is eligible for a discount.")
    )
    final_fee = models.IntegerField(
        _("Final Fee"),
        default=0,
        help_text=_("The final fee the participant needs to pay.")
    )
    payment_status = models.IntegerField(
        _("Payment status"),
        choices=constants.PAYMENT_STATUS,
        default=0,
        help_text=_("The status of the participant's payment for the course.")
    )
    payment_method = models.IntegerField(
        _("Payment method"),
        choices=constants.PAYMENT_METHODS,
        default=0,
        help_text=_(
            "The method by which the participant will make the payment.")
    )
    comment = models.TextField(
        _("Comment"),
        blank=True,
        help_text=_(
            "Any additional comments or notes regarding the registration.")
    )
    dinner = models.BooleanField(
        _("Dinner"),
        blank=True,
        null=True,
        help_text=_("Indicates whether the participant will attend the dinner.")
    )
    overnight_stay = models.BooleanField(
        _("Overnight stay"),
        blank=True,
        null=True,
        help_text=_(
            "Indicates whether the participant needs a place to stay overnight.")
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_registration",
                condition=models.Q(user__isnull=False)
            ),
            models.UniqueConstraint(
                fields=["email", "course"],
                name="unique_guest_registration",
                condition=models.Q(email__isnull=False)
            )
        ]
        verbose_name = _("Course Registration")
        verbose_name_plural = _("Course Registrations")

    def calculate_fees(self, course, selected_sessions):
        final_fee = 0
        if len(selected_sessions) == len(course.sessions.all()):
            final_fee = course.course_fee if self.payment_method == 0 else course.course_fee_cash
        else:
            for session in selected_sessions:
                final_fee += session.session_fee if self.payment_method == 0 else session.session_fee_cash
        return final_fee * course.discount_percentage / 100 if self.discount else final_fee

    def set_exam(self, user=None):
        if self.exam:
            if self.user:
                user_profile = get_object_or_404(UserProfile, user=user)
                if user_profile.grade < 6:
                    self.exam_grade = user_profile.grade + 1
                else:
                    self.exam = False
            else:
                if self.grade < 6:
                    self.exam_grade = self.grade + 1
                else:
                    self.exam = False

    def save(self, *args, **kwargs):
        if not self.course.course_type == "international":
            self.dinner = None
            self.overnight_stay = None

        if self.email and self.dojo == "other":
            self.dojo = self.other_dojo

        if self.user:
            self.email = self.user.email
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
            user_profile = get_object_or_404(UserProfile, user=self.user)
            self.dojo = user_profile.dojo
            self.grade = user_profile.grade
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
