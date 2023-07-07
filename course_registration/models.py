from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

REGISTRATION_STATUS = ((0, "Closed"), (1, "Open"))
PAYMENT_STATUS = ((0, "Unpaid"), (1, "Paid"))


class Course(models.Model):
    """Represents a course user can sign up for"""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    registration_status = models.IntegerField(
        choices=REGISTRATION_STATUS, default=0
    )
    course_fee = models.IntegerField()

    class Meta:
        ordering = ["start_date"]

    def __str__(self):
        return self.title

    # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.clean
    def clean(self):
        """Custom validation for Course model"""
        if (
            self.start_date
            and self.end_date
            and self.start_date > self.end_date
        ):
            raise ValidationError("Start date cannot be later than end date.")


class CourseSession(models.Model):
    """Represents a session within a course"""

    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    session_fee = models.IntegerField(default=10)

    def __str__(self):
        return f"{self.date}: {self.title}"

    # https://docs.djangoproject.com/en/4.2/ref/models/instances/#django.db.models.Model.clean
    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError("Start time cannot be later than end time.")


class CourseRegistration(models.Model):
    """Represents a registration for a course by a user"""

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    selected_sessions = models.ManyToManyField(CourseSession, blank=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    exam = models.BooleanField(default=False)
    accept_terms = models.BooleanField(default=False)
    final_fee = models.IntegerField()
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=0)
    comment = models.TextField(blank=True)

    class Meta:
        # https://docs.djangoproject.com/en/4.2/ref/models/constraints/#django.db.models.UniqueConstraint
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_user_registration"
            )
        ]
