from django.urls import path

from . import views

urlpatterns = [
    path(
        "courses/register/<slug:slug>/",
        views.RegisterCourse.as_view(),
        name="register_course",
    ),
    path(
        "user/registrations/",
        views.UserCourseRegistrationList.as_view(),
        name="courseregistration_list",
    ),
    path(
        "user/registrations/cancel/<int:pk>/",
        views.CancelUserCourseRegistration.as_view(),
        name="cancel_courseregistration",
    ),
    path(
        "user/registrations/update/<int:pk>/",
        views.UpdateUserCourseRegistration.as_view(),
        name="update_courseregistration",
    ),
]
