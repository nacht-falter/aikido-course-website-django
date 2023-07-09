from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Course(models.Model):
    """Represents a course a user can sign up for"""

    REGISTRATION_STATUS = ((0, "Closed"), (1, "Open"))

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

    # https://docs.djangoproject.com/en/4.2/ref/models/instances
    # /#django.db.models.Model.clean
    def clean(self):
        if self.start_time > self.end_time:
            raise ValidationError("Start time cannot be later than end time.")


class CourseRegistration(models.Model):
    """Represents a registration for a course by a user"""

    PAYMENT_STATUS = ((0, "Unpaid"), (1, "Paid"))

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
        # Set unique constraint: https://docs.djangoproject.com/en/4.2/
        # ref/models/constraints/#django.db.models.UniqueConstraint
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"], name="unique_user_registration"
            )
        ]


class UserProfile(models.Model):
    """Represents a user profile"""

    # Documentation for defing choices for a CharField
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
    NO_GRADE = "ng"
    SIXTH_KYU = "6k"
    FIFTH_KYU = "5k"
    FOURTH_KYU = "4k"
    THIRD_KYU = "3k"
    SECOND_KYU = "2k"
    FIRST_KYU = "1k"
    SHODAN = "1d"
    NIDAN = "2d"
    SANDAN = "3d"
    YONDAN = "4d"
    GODAN = "5d"
    ROKUDAN = "6d"

    GRADES_CHOICES = [
        (NO_GRADE, "No Grade (Red Belt)"),
        (SIXTH_KYU, "6. Kyu (White Belt)"),
        (FIFTH_KYU, "5. Kyu (Yellow Belt)"),
        (FOURTH_KYU, "4. Kyu (Orange Belt)"),
        (THIRD_KYU, "3. Kyu (Green Belt)"),
        (SECOND_KYU, "2. Kyu (Blue Belt)"),
        (FIRST_KYU, "1. Kyu (Brown Belt)"),
        (SHODAN, "1. Dan"),
        (NIDAN, "2. Dan"),
        (SANDAN, "3. Dan"),
        (YONDAN, "4. Dan"),
        (GODAN, "5. Dan"),
        (ROKUDAN, "6. Dan"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    grade = models.CharField(
        max_length=2, choices=GRADES_CHOICES, default=NO_GRADE
    )

    # Overriding save method: https://docs.djangoproject.com/en/4.2
    # /topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        # Create slug from another field: https://stackoverflow.com/a/837835
        if not self.id:
            self.slug = slugify(self.user.username)

            self.user.first_name = self.first_name
            self.user.last_name = self.last_name
            self.user.save()

        super(UserProfile, self).save(*args, **kwargs)
