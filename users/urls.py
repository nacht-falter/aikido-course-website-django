from django.urls import path

from .views import CustomPasswordChangeView

from . import views

urlpatterns = [
    path(
        "user/profile/",
        views.UserProfileView.as_view(),
        name="userprofile",
    ),
    path(
        "user/profile/update/",
        views.UpdateUserProfile.as_view(),
        name="update_userprofile",
    ),
    path(
        "user/deactivate/",
        views.DeactivateUser.as_view(),
        name="deactivate_user",
    ),
    path(
        "user/update-grade/",
        views.UpdateGrade.as_view(),
        name="update_grade",
    ),
    # Override default allauth password redirect url
    # https://stackoverflow.com/a/56599071
    path(
        "accounts/password/change/",
        CustomPasswordChangeView.as_view(),
        name="account_change_password",
    ),
]
