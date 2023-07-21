from django.urls import path

from course_registration.views import CustomPasswordChangeView

from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("courses/", views.CourseList.as_view(), name="course_list"),
    path(
        "courses/register/<slug:slug>/",
        views.RegisterCourse.as_view(),
        name="register_course",
    ),
    path(
        "user/registrations/",
        views.CourseRegistrationList.as_view(),
        name="courseregistration_list",
    ),
    path(
        "user/registrations/cancel/<int:pk>/",
        views.CancelCourseRegistration.as_view(),
        name="cancel_courseregistration",
    ),
    path(
        "user/registrations/update/<int:pk>/",
        views.UpdateCourseRegistration.as_view(),
        name="update_courseregistration",
    ),
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
    path(
        "pages/<slug:category_slug>/<slug:page_slug>/",
        views.PageDetail.as_view(),
        name="page_detail",
    ),
    # Override default allauth password redirect url
    # https://stackoverflow.com/a/56599071
    path(
        "accounts/password/change/",
        CustomPasswordChangeView.as_view(),
        name="account_change_password",
    ),
]
