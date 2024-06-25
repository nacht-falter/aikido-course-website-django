from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from danbw_website import constants


class User(AbstractUser):
    def __str__(self):
        return self.first_name + " " + self.last_name


class UserProfile(models.Model):
    """Represents a user profile"""

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    slug = models.SlugField(unique=True)
    dojo = models.CharField(
        _("Dojo"), max_length=5, choices=constants.DOJO_CHOICES)
    other_dojo = models.CharField(_("Other Dojo"), max_length=100, blank=True)
    grade = models.IntegerField(
        _("Grade"), choices=constants.GRADE_CHOICES, default=constants.RED_BELT)

    # Overriding save method: https://docs.djangoproject.com/en/4.2
    # /topics/db/models/#overriding-predefined-model-methods
    def save(self, *args, **kwargs):
        # Create slug from another field: https://stackoverflow.com/a/837835
        if not self.slug:
            self.slug = slugify(
                f"{self.user.first_name}-{self.user.last_name}")
        super().save(*args, **kwargs)
