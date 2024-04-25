from cloudinary.models import CloudinaryField
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

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

(
    BANK,
    CASH,
) = range(2)

PAYMENT_STATUS = ((0, "Unpaid"), (1, "Paid"))

PAYMENT_METHODS = [
    (BANK, "Bank Transfer"),
    (CASH, "Cash"),
]

EXAM_GRADE_CHOICES = [
    (SIXTH_KYU, "7th Kyu ⚪️"),
    (FIFTH_KYU, "5th Kyu 🟡"),
    (FOURTH_KYU, "4th Kyu 🟠"),
    (THIRD_KYU, "3rd Kyu 🟢"),
    (SECOND_KYU, "2nd Kyu 🔵"),
    (FIRST_KYU, "1st Kyu 🟤"),
]

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

DOJO_CHOICES = [
    ("AAR", "Aikido am Rhein"),
    ("AVE", "Aikido Verein Emmendingen"),
    ("AVF", "Aikido Verein Freiburg"),
    ("TVD", "Turnverein Denzlingen"),
]


class User(AbstractUser):
    pass


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
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    session_fee = models.IntegerField(default=0)
    session_fee_cash = models.IntegerField(default=0)

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


class UserCourseRegistration(models.Model):
    """Represents a registration for a course by a user"""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="registrations"
    )
    course = models.ForeignKey(InternalCourse, on_delete=models.CASCADE)
    selected_sessions = models.ManyToManyField(CourseSession, blank=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    exam = models.BooleanField(default=False)
    exam_grade = models.IntegerField(
        choices=EXAM_GRADE_CHOICES, default=RED_BELT
    )
    exam_passed = models.BooleanField(null=True)
    grade_updated = models.BooleanField(default=False)
    accept_terms = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    final_fee = models.IntegerField(default=0)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=0)
    payment_method = models.IntegerField(choices=PAYMENT_METHODS, default=0)
    comment = models.TextField(blank=True)

    class Meta:
        # Set unique constraint: https://docs.djangoproject.com/en/4.2/
        # ref/models/constraints/#django.db.models.UniqueConstraint
        constraints = [
            models.UniqueConstraint(
                fields=["user", "course"],
                name="unique_user_registration"
            )
        ]

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


class GuestCourseRegistration(models.Model):
    """Represents a registration for a course by a user"""

    email = models.EmailField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    course = models.ForeignKey(InternalCourse, on_delete=models.CASCADE)
    selected_sessions = models.ManyToManyField(CourseSession, blank=False)
    registration_date = models.DateTimeField(auto_now_add=True)
    dojo = models.CharField(max_length=3, choices=DOJO_CHOICES, blank=False)
    grade = models.IntegerField(
        choices=GRADE_CHOICES, default=RED_BELT, blank=False)
    exam = models.BooleanField(default=False)
    exam_grade = models.IntegerField(
        choices=EXAM_GRADE_CHOICES, blank=True, null=True
    )
    accept_terms = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    final_fee = models.IntegerField(default=0)
    payment_status = models.IntegerField(choices=PAYMENT_STATUS, default=0)
    payment_method = models.IntegerField(choices=PAYMENT_METHODS, default=0)
    comment = models.TextField(blank=True)

    class Meta:
        # Set unique constraint: https://docs.djangoproject.com/en/4.2/
        # ref/models/constraints/#django.db.models.UniqueConstraint
        constraints = [
            models.UniqueConstraint(
                fields=["email", "course"],
                name="unique_guest_registration"
            )
        ]

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


class UserProfile(models.Model):
    """Represents a user profile"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    slug = models.SlugField(unique=True)
    dojo = models.CharField(max_length=3, choices=DOJO_CHOICES)
    grade = models.IntegerField(choices=GRADE_CHOICES, default=RED_BELT)

    # Overriding save method: https://docs.djangoproject.com/en/4.2
    # /topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        # Create slug from another field: https://stackoverflow.com/a/837835
        if not self.slug:
            self.slug = slugify(
                f"{self.user.first_name}-{self.user.last_name}")
        super(UserProfile, self).save(*args, **kwargs)


class Category(models.Model):
    """Represents a category to be used for displaying pages on the website"""

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    menu_position = models.IntegerField(default=0)

    class Meta:
        # https://djangoandy.com/2021/09/01/adjusting-the-plural-of-a-
        # model-in-django-admin/
        verbose_name_plural = "categories"
        ordering = ["menu_position"]

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
    menu_position = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["menu_position"]
