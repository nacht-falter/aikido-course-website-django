from django.urls import re_path

from . import views
from .views import CustomPasswordChangeView

urlpatterns = [
    # User profile view
    re_path(r"^user/profile/?$",
            views.UserProfileView.as_view(), name="userprofile"),

    # Update user profile view
    re_path(r"^user/profile/update/?$",
            views.UpdateUserProfile.as_view(), name="update_userprofile"),

    # Deactivate user view
    re_path(r"^user/deactivate/?$", views.DeactivateUser.as_view(),
            name="deactivate_user"),

    # Update grade view
    re_path(r"^user/update-grade/?$",
            views.UpdateGrade.as_view(), name="update_grade"),

    # Custom password change view
    re_path(r"^accounts/password/change/?$",
            CustomPasswordChangeView.as_view(), name="account_change_password"),
]
