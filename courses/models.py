from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from danbw_website import constants


class Course(models.Model):
    """Represents a course a user can sign up for"""

    title = models.CharField(
        _("Title"),
        max_length=200,
        help_text=_("The name of the course.")
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )
    start_date = models.DateField(
        _("Start Date"),
        default=date.today,
        help_text=_("The start date of the course.")
    )
    end_date = models.DateField(
        _("End Date"),
        default=date.today,
        help_text=_("The end date of the course.")
    )
    teacher = models.CharField(
        _("Teacher(s)"),
        max_length=200,
        blank=True,
        help_text=_("The teacher(s) of the course (optional).")
    )

    class Meta:
        ordering = ["start_date"]
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title

    def get_course_type(self):
        return self.__class__.__name__

    def clean(self):
        """Custom validation for Course model"""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError(
                _("Start date cannot be later than end date."))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class InternalCourse(Course):
    """Represents a course organized by the organization"""

    REGISTRATION_STATUS = (
        (0, _("closed")),
        (1, _("open")),
    )

    COURSE_TYPE = (
        ("regional", _("Regional Course")),
        ("international", _("International Course")),
        ("family_reunion", _("Family Reunion")),
    )

    STATUS_CHOICES = (
        (0, _("Preview")),
        (1, _("Published")),
    )

    status = models.IntegerField(
        _("Status"),
        choices=STATUS_CHOICES,
        default=0,
        help_text=_(
            "Courses set to 'Preview' will appear in the course list without all details.")
    )
    publication_date = models.DateField(
        _("Publication Date"),
        blank=True,
        null=True,
        help_text=_(
            "If this date is set, the course will automatically be set to 'Published' on this date.")
    )
    registration_status = models.IntegerField(
        _("Registration Status"),
        choices=REGISTRATION_STATUS,
        default=0,
        help_text=_(
            "If the registration status is set to 'open', users can sign up for the course.")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("A short description of the course (optional).")
    )
    location = models.CharField(
        _("Location"),
        max_length=200,
        blank=True,
        help_text=_("The location of the course (optional).")
    )
    registration_start_date = models.DateField(
        _("Registration Start Date"),
        blank=True,
        null=True,
        help_text=_(
            "If this date is set, the registration status will be automatically set to 'open' on this date.")
    )
    registration_end_date = models.DateField(
        _("Registration End Date"),
        blank=True,
        null=True,
        help_text=_(
            "If this date is set, the registration status will be automatically set to 'closed' on this date.")
    )
    organizer = models.CharField(
        _("Organizer"),
        max_length=200,
        blank=True,
        default="D.A.N. BW",
        help_text=_("The organizer of the course (optional).")
    )
    course_fee = models.IntegerField(
        _("Course Fee"),
        default=0,
        help_text=_(
            "The fee for the entire course (payments via bank transfer).")
    )
    course_fee_cash = models.IntegerField(
        _("Course Fee (Cash)"),
        default=0,
        help_text=_("The fee for the entire course (cash payments).")
    )
    discount_percentage = models.IntegerField(
        _("Discount Percentage"),
        default=50,
        help_text=_(
            "The discount percentage specified here will automatically be applied for users eligible for a discount.")
    )
    bank_transfer_until = models.DateField(
        _("Bank Transfer Until"),
        default=date.today,
        help_text=_(
            "The date until which the course fee has to be paid via bank transfer.")
    )
    course_type = models.CharField(
        _("Course Type"),
        choices=COURSE_TYPE,
        max_length=200,
        help_text=_(
            "The type of the course will determine which fields will be displayed in the registration form.")
    )
    flyer = models.ImageField(
        _("Flyer"),
        upload_to="images/",
        blank=True,
        null=True,
        help_text=_(
            "The course flyer. Needs to be uploaded as an image file (JPEG, PNG, etc.).")
    )
    additional_info = models.TextField(
        _("Additional Information"),
        blank=True,
        help_text=_("Additional information about the course (optional).")
    )

    def clean(self):
        """Custom validation for Internal Course model"""
        super().clean()
        if self.registration_start_date and self.registration_end_date:
            if self.registration_start_date > self.registration_end_date:
                raise ValidationError(
                    _("Registration start date cannot be later than registration end date."))

    def save(self, *args, **kwargs):
        if self.registration_start_date or self.registration_end_date:
            start_ok = self.registration_start_date is None or self.registration_start_date <= date.today()
            end_ok = self.registration_end_date is None or date.today() <= self.registration_end_date

            if start_ok and end_ok:
                self.registration_status = 1
            else:
                self.registration_status = 0

        if self.publication_date and self.publication_date <= date.today():
            self.status = 1

        if self.end_date < date.today():
            self.status = 0
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Internal Course")
        verbose_name_plural = _("Internal Courses")


class ExternalCourse(Course):
    """Represents a course organized by an external organization"""

    organizer = models.CharField(
        _("Organizer"),
        max_length=200,
        blank=True,
        help_text=_("The organizer of the course (optional).")
    )
    url = models.URLField(_("URL"))

    class Meta:
        verbose_name = _("External Course")
        verbose_name_plural = _("External Courses")


class CourseSession(models.Model):
    """Represents a session within a course"""

    title = models.CharField(
        _("Title"),
        max_length=200,
        help_text=_("The name of the session.")
    )
    course = models.ForeignKey(
        InternalCourse,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("Course"),
        help_text=_("The course to which this session belongs.")
    )
    date = models.DateField(
        _("Date"),
        default=date.today,
        help_text=_("The date on which the session takes place.")
    )
    start_time = models.TimeField(
        _("Start Time"),
        default="00:00",
        help_text=_("The time at which the session starts.")
    )
    end_time = models.TimeField(
        _("End Time"),
        default="00:00",
        help_text=_("The time at which the session ends.")
    )
    session_fee = models.IntegerField(
        _("Session Fee"),
        default=0,
        help_text=_(
            "The fee for attending this session if paid via bank transfer.")
    )
    session_fee_cash = models.IntegerField(
        _("Session Fee (Cash)"),
        default=0,
        help_text=_("The fee for attending this session if paid in cash.")
    )

    def __str__(self):
        return f"{constants.WEEKDAYS[self.date.weekday()][1]}, {self.date.strftime('%d.%m.%Y')}, {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}: {self.title}"

    def clean(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValidationError(
                _("Start time cannot be later than end time."))

    class Meta:
        verbose_name = _("Course Session")
        verbose_name_plural = _("Course Sessions")
