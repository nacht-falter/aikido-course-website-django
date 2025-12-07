from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from danbw_website import constants
from fees.models import Fee


class Course(models.Model):
    """Represents a course a user can sign up for"""

    title = models.CharField(
        _("Title"),
        max_length=200,
    )
    slug = models.SlugField(
        max_length=200,
        unique=True
    )
    start_date = models.DateField(
        _("Start Date"),
        default=date.today,
    )
    end_date = models.DateField(
        _("End Date"),
        default=date.today,
    )
    teacher = models.CharField(
        _("Teacher(s)"),
        max_length=200,
        blank=True,
    )

    class Meta:
        ordering = ["start_date"]
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def _generate_unique_slug(self):
        slug = slugify(self.title)

        if self.slug and self.slug.startswith(slug):
            return self.slug

        unique_slug = slug
        num = 1

        while Course.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
            unique_slug = f'{slug}-{num}'
            num += 1

        return unique_slug

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
        self.slug = self._generate_unique_slug()
        super().save(*args, **kwargs)


class InternalCourse(Course):
    """Represents a course organized by the organization"""

    REGISTRATION_STATUS = (
        (0, _("closed")),
        (1, _("open")),
    )

    STATUS_CHOICES = (
        (0, _("Preview")),
        (1, _("Published")),
    )

    status = models.IntegerField(
        _("Status"),
        choices=STATUS_CHOICES,
        default=0,
    )
    publication_date = models.DateField(
        _("Publication Date"),
        blank=True,
        null=True,
    )
    registration_status = models.IntegerField(
        _("Registration Status"),
        choices=REGISTRATION_STATUS,
        default=0,
    )
    description = models.TextField(
        _("Description"),
        blank=True,
    )
    location = models.CharField(
        _("Location"),
        max_length=200,
        blank=True,
    )
    registration_start_date = models.DateField(
        _("Registration Start Date"),
        blank=True,
        null=True,
    )
    registration_end_date = models.DateField(
        _("Registration End Date"),
        blank=True,
        null=True,
    )
    organizer = models.CharField(
        _("Organizer"),
        max_length=200,
        blank=True,
        default="D.A.N. BW",
    )
    discount_percentage = models.IntegerField(
        _("Discount Percentage"),
        default=50,
        help_text=_("Discount for economically disadvantaged groups"),
    )
    bank_transfer_until = models.DateField(
        _("Bank Transfer Until"),
        default=date.today,
        blank=True,
        null=True,
    )
    course_type = models.CharField(
        _("Course Type"),
        choices=constants.COURSE_TYPES,
        max_length=100,
    )
    fee_category = models.CharField(
        _("Fee Category"),
        choices=constants.FEE_CATEGORIES,
        max_length=100,
    )
    flyer = models.ImageField(
        _("Flyer"),
        upload_to="images/",
        blank=True,
        null=True,
    )
    additional_info = models.TextField(
        _("Additional Information"),
        blank=True,
    )
    dan_discount = models.BooleanField(
        _("Course with D.A.N. Member Discount"),
        default=False,
        help_text=_("D.A.N. members receive a discount on this course."),
    )
    has_dan_preparation = models.BooleanField(
        _("Course with Dan Preparation"),
        default=False,
    )
    has_dinner = models.BooleanField(
        _("Course with Dinner"),
        default=False,
    )

    def clean(self):
        """Custom validation for Internal Course model"""
        super().clean()
        if self.registration_start_date and self.registration_end_date:
            if self.registration_start_date > self.registration_end_date:
                raise ValidationError(
                    _("Registration start date cannot be later than registration end date."))

        if not Fee.objects.filter(
            course_type=self.course_type,
            fee_category=self.fee_category,
        ).exists():
            raise ValidationError(
                _(f"No fee found for course type '{self.course_type}' and fee category '{self.fee_category}' found.")
            )

        if (
            self.dan_discount and (
                self.course_type not in constants.INTERNATIONAL_COURSES or self.fee_category == "dan_seminar")
        ):
            raise ValidationError(
                _("D.A.N. member discount not applicable for this course type/fee category.")
            )

        if self.registration_status == 1 and self.course_type == "children":
            raise ValidationError(
                _("Online Registration for children's courses is not allowed. Please change the registration status to 'closed'.")
            )

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

        if self.has_dan_preparation and self.course_type not in constants.DAN_PREPARATION_COURSES:
            self.has_dan_preparation = False

        super().save(*args, **kwargs)

    def update_has_dan_preparation(self):
        has_dan_preparation = self.sessions.filter(
            is_dan_preparation=True).exists()

        if self.course_type in constants.DAN_PREPARATION_COURSES:
            if self.has_dan_preparation != has_dan_preparation:
                self.has_dan_preparation = has_dan_preparation
                self.save()

    class Meta:
        verbose_name = _("Internal Course")
        verbose_name_plural = _("Internal Courses")


class ExternalCourse(Course):
    """Represents a course organized by an external organization"""

    organizer = models.CharField(
        _("Organizer"),
        max_length=200,
        blank=True,
    )
    url = models.URLField(_("URL"), blank=True)

    class Meta:
        verbose_name = _("External Course")
        verbose_name_plural = _("External Courses")


class CourseSession(models.Model):
    """Represents a session within a course"""

    title = models.CharField(
        _("Title"),
        max_length=200,
    )
    course = models.ForeignKey(
        InternalCourse,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name=_("Course"),
    )
    date = models.DateField(
        _("Date"),
        default=date.today,
    )
    start_time = models.TimeField(
        _("Start Time"),
        default="00:00",
    )
    end_time = models.TimeField(
        _("End Time"),
        default="00:00",
    )
    is_dan_preparation = models.BooleanField(
        _("Dan Preparation"),
        default=False,
    )

    def __str__(self):
        return f"{constants.WEEKDAYS[self.date.weekday()][1]}, {self.date.strftime('%d.%m.%Y')}, {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}: {self.title}"

    def clean(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValidationError(
                _("Start time cannot be later than end time."))

        if self.is_dan_preparation and not self.course.course_type in constants.DAN_PREPARATION_COURSES:
            raise ValidationError(
                _("Dan preparation sessions are not allowed on this course."))

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.course.update_has_dan_preparation()

    class Meta:
        ordering = ["date", "start_time"]
        verbose_name = _("Course Session")
        verbose_name_plural = _("Course Sessions")


class AccommodationOption(models.Model):
    """Accommodation option for a course (e.g., for Family Reunion courses)"""

    course = models.ForeignKey(
        InternalCourse,
        on_delete=models.CASCADE,
        related_name="accommodation_options",
        verbose_name=_("Course"),
    )
    name = models.CharField(
        _("Name"),
        max_length=200,
        help_text=_("e.g., 'No accommodation', '2 nights', 'Full week'"),
    )
    fee = models.DecimalField(
        _("Fee"),
        max_digits=10,
        decimal_places=2,
        default=0,
        help_text=_("Additional fee for this accommodation option"),
    )
    order = models.IntegerField(
        _("Order"),
        default=0,
        help_text=_("Display order (lower numbers appear first)"),
    )

    class Meta:
        ordering = ["order", "id"]
        verbose_name = _("Accommodation Option")
        verbose_name_plural = _("Accommodation Options")

    def __str__(self):
        return f"{self.name} ({self.fee}€)"
