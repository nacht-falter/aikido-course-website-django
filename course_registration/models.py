from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from cloudinary.models import CloudinaryField

# Documentation for defining choices for CharFields:
# https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
# Assign increasing integer values to a list of variables:
# https://stackoverflow.com/a/64485228
(
    RED_BELT,
    SIXTH_KYU,
    FIFTH_KYU,
    FOURTH_KYU,
    THIRD_KYU,
    SECOND_KYU,
    FIRST_KYU,
    SHODAN,
    NIDAN,
    SANDAN,
    YONDAN,
    GODAN,
    ROKUDAN,
) = range(13)


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
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="sessions"
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    session_fee = models.IntegerField(default=10)

    def __str__(self):
        return self.title

    # https://docs.djangoproject.com/en/4.2/ref/models/instances
    # /#django.db.models.Model.clean
    def clean(self):
        if (
            self.start_time
            and self.end_time
            and self.start_time > self.end_time
        ):
            raise ValidationError("Start time cannot be later than end time.")


class CourseRegistration(models.Model):
    """Represents a registration for a course by a user"""

    PAYMENT_STATUS = ((0, "Unpaid"), (1, "Paid"))

    EXAM_GRADE_CHOICES = [
        (SIXTH_KYU, "6th Kyu ⚪️"),
        (FIFTH_KYU, "5th Kyu 🟡"),
        (FOURTH_KYU, "4th Kyu 🟠"),
        (THIRD_KYU, "3rd Kyu 🟢"),
        (SECOND_KYU, "2nd Kyu 🔵"),
        (FIRST_KYU, "1st Kyu 🟤"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    selected_sessions = models.ManyToManyField(CourseSession, blank=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    exam = models.BooleanField(default=False)
    exam_grade = models.IntegerField(
        choices=EXAM_GRADE_CHOICES, default=RED_BELT
    )
    exam_passed = models.BooleanField(null=True)
    grade_updated = models.BooleanField(default=False)
    accept_terms = models.BooleanField(default=False)
    final_fee = models.IntegerField(default=0)
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

    GRADE_CHOICES = [
        (RED_BELT, "Red Belt 🔴"),
        (SIXTH_KYU, "6th Kyu ⚪️"),
        (FIFTH_KYU, "5th Kyu 🟡"),
        (FOURTH_KYU, "4th Kyu 🟠"),
        (THIRD_KYU, "3rd Kyu 🟢"),
        (SECOND_KYU, "2nd Kyu 🔵"),
        (FIRST_KYU, "1st Kyu 🟤"),
        (SHODAN, "1st Dan ⚫️"),
        (NIDAN, "2nd  Dan ⚫️"),
        (SANDAN, "3rd Dan ⚫️"),
        (YONDAN, "4th Dan ⚫️"),
        (GODAN, "5th Dan ⚫️"),
        (ROKUDAN, "6th Dan ⚫️"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True)
    grade = models.IntegerField(choices=GRADE_CHOICES, default=RED_BELT)

    # Overriding save method: https://docs.djangoproject.com/en/4.2
    # /topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        # Create slug from another field: https://stackoverflow.com/a/837835
        if not self.slug:
            self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)


class Category(models.Model):
    """Represents a category to be used for displaying pages on the website"""

    title = models.CharField(max_length=200, unique=True)

    class Meta:
        # https://djangoandy.com/2021/09/01/adjusting-the-plural-of-a-
        # model-in-django-admin/
        verbose_name_plural = "categories"

    def __str__(self):
        return self.title


class Page(models.Model):
    """Represents a page to be displayed on the website"""

    STATUS = ((0, "Draft"), (1, "Published"))

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="pages"
    )
    status = models.IntegerField(choices=STATUS, default=0)
    featured_image = CloudinaryField("image", default="placeholder")
    content = models.TextField()

    def __str__(self):
        return self.title
