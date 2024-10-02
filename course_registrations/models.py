from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.html import format_html
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
        null=True,
        blank=True
    )
    email = models.EmailField(
        _("Email"),
        null=True,
        blank=True
    )
    first_name = models.CharField(
        _("First Name"),
        max_length=100,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        _("Last Name"),
        max_length=100,
        null=True,
        blank=True
    )
    course = models.ForeignKey(
        InternalCourse,
        on_delete=models.CASCADE,
        verbose_name=_("Course"),
    )
    selected_sessions = models.ManyToManyField(
        CourseSession,
        blank=False,
        verbose_name=_("Selected sessions"),
    )
    registration_date = models.DateTimeField(
        _("Registration date"),
        auto_now_add=True,
    )
    dojo = models.CharField(
        _("Dojo"),
        max_length=100,
        blank=True,
        null=True,
    )
    grade = models.IntegerField(
        _("Grade"),
        choices=constants.GRADE_CHOICES,
        default=constants.RED_BELT,
        blank=True,
        null=True,
    )
    exam = models.BooleanField(
        _("Exam"),
        default=False,
        null=True,
    )
    exam_grade = models.IntegerField(
        _("Exam Grade"),
        choices=constants.EXAM_GRADE_CHOICES,
        blank=True,
        null=True,
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
    )
    discount = models.BooleanField(
        _("Discount"),
        default=False,
    )
    final_fee = models.IntegerField(
        _("Final Fee"),
        default=0,
    )
    payment_status = models.IntegerField(
        _("Payment status"),
        choices=constants.PAYMENT_STATUS,
        default=0,
    )
    payment_method = models.IntegerField(
        _("Payment method"),
        choices=constants.PAYMENT_METHODS,
        default=0,
    )
    comment = models.TextField(
        _("Comment"),
        blank=True,
    )
    dinner = models.BooleanField(
        _("Dinner"),
        blank=True,
        null=True,
    )
    overnight_stay = models.BooleanField(
        _("Overnight stay"),
        blank=True,
        null=True,
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
        all_sessions = course.sessions.all()
        count_dan_preparation = sum(
            1 for session in all_sessions if session.is_dan_preparation)

        if len(selected_sessions) == len(all_sessions):
            if course.course_type == "international":
                final_fee = (
                    course.course_fee_with_dan_preparation
                    if self.payment_method == 0
                    else course.course_fee_with_dan_preparation_cash
                )
            else:
                final_fee = course.course_fee if self.payment_method == 0 else course.course_fee_cash
        elif len(selected_sessions) == len(all_sessions) - count_dan_preparation:
            final_fee = course.course_fee if self.payment_method == 0 else course.course_fee_cash
        else:
            for session in selected_sessions:
                final_fee += session.session_fee if self.payment_method == 0 else session.session_fee_cash

        return final_fee * (1 - course.discount_percentage / 100) if self.discount else final_fee

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

    def truncated_session_display(self):
        all_sessions = self.course.sessions.all()
        if len(self.selected_sessions.all()) == len(all_sessions):
            return _("Entire Course")
        else:
            sessions = "\n".join([str(session) for session in self.selected_sessions.all()])
            truncated = sessions[:30] + \
                "..." if len(sessions) > 30 else sessions
            return format_html('<span title="{}">{}</span>', sessions, truncated)
    truncated_session_display.short_description = _("Selected Sessions")

    def truncated_comment(self):
        if self.comment:
            truncated = self.comment[:30] + \
                "..." if len(self.comment) > 30 else self.comment
            return format_html('<span title="{}">{}</span>', self.comment, truncated)
        return ""
    truncated_comment.short_description = _("Comment")
