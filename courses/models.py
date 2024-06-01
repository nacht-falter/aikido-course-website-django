from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify

from danbw_website import constants


class Course(models.Model):
    """Represents a course a user can sign up for"""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(default=date.today)
    teacher = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.title

    def get_course_type(self):
        return self.__class__.__name__

    # https://docs.djangoproject.com/en/4.2/ref/models/instances
    # /#django.db.models.Model.clean
    def clean(self):
        """Custom validation for Course model"""
        if (
            self.start_date
            and self.end_date
            and self.start_date > self.end_date
        ):
            raise ValidationError("Start date cannot be later than end date.")

        if (self.registration_start_date
                and self.registration_end_date
                and self.registration_start_date > self.registration_end_date
                ):
            raise ValidationError(
                "Registration start date cannot be later than registration end date.")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class InternalCourse(Course):
    """Represents a course organized by the organization"""

    REGISTRATION_STATUS = ((0, "Closed"), (1, "Open"))

    COURSE_TYPE = (
        ("regional", "Regional Course"),
        ("international", "International Course"),
        ("family_reunion", "Family Reunion"),
    )

    STATUS_CHOICES = ((0, "Preview"), (1, "Published"))

    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    registration_status = models.IntegerField(
        choices=REGISTRATION_STATUS, default=0
    )
    description = models.TextField(blank=True)
    registration_start_date = models.DateField(blank=True)
    registration_end_date = models.DateField(blank=True)
    organizer = models.CharField(max_length=200, blank=True, default="DANBW")
    course_fee = models.IntegerField(default=0)
    course_fee_cash = models.IntegerField(default=0)
    discount_percentage = models.IntegerField(default=50)
    bank_transfer_until = models.DateField(default=date.today)
    course_type = models.CharField(choices=COURSE_TYPE, max_length=200)
    additional_info = models.TextField("Additional information", blank=True)

    def save(self, *args, **kwargs):
        if self.registration_start_date <= date.today() <= self.registration_end_date:
            self.registration_status = 1  # Open
        else:
            self.registration_status = 0  # Closed
        super().save(*args, **kwargs)


class ExternalCourse(Course):
    """Represents a course organized by an external organization"""

    organizer = models.CharField(max_length=200, blank=True)
    url = models.URLField()


class CourseSession(models.Model):
    """Represents a session within a course"""

    title = models.CharField(max_length=200)
    course = models.ForeignKey(
        InternalCourse, on_delete=models.CASCADE, related_name="sessions"
    )
    date = models.DateField(default=date.today)
    start_time = models.TimeField(default="00:00")
    end_time = models.TimeField(default="00:00")
    session_fee = models.IntegerField(default=0)
    session_fee_cash = models.IntegerField(default=0)

    def __str__(self):
        return f"{constants.WEEKDAYS[self.date.weekday()][1]}, {self.date.strftime('%d.%m.%Y')}, {self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}: {self.title}"

    # https://docs.djangoproject.com/en/4.2/ref/models/instances
    # /#django.db.models.Model.clean
    def clean(self):
        if (
            self.start_time
            and self.end_time
            and self.start_time > self.end_time
        ):
            raise ValidationError("Start time cannot be later than end time.")
