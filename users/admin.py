from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserProfile

admin.site.register(User, UserAdmin)


class UserProfileInline(admin.StackedInline):
    """Displays UserProfile as an inline model"""

    model = UserProfile
    extra = 0  # Set number of additional rows to 0
    fields = ["grade", "dojo"]


# Add inlines to UserAdmin model: https://stackoverflow.com/a/35573797
UserAdmin.inlines += (UserProfileInline,)
