from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify


class Course(models.Model):
    """Represents a course a user can sign up for"""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class InternalCourse(Course):
    """Represents a course organized by the organization"""

    REGISTRATION_STATUS = ((0, "Closed"), (1, "Open"))

    registration_status = models.IntegerField(
        choices=REGISTRATION_STATUS, default=0
    )
    description = models.TextField(blank=True)
    registration_start_date = models.DateField(blank=True)
    registration_end_date = models.DateField(blank=True)
    organizer = models.CharField(max_length=200, blank=True, default="DANBW")
    course_fee = models.IntegerField()
    course_fee_cash = models.IntegerField()
    discount_percentage = models.IntegerField(default=50)
    bank_transfer_until = models.DateField(blank=False)

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
