from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^courses/register/(?P<slug>[\w-]+)/?$",
        views.RegisterCourse.as_view(),
        name="register_course",
    ),
    re_path(
        r"^user/registrations/?$",
        views.CourseRegistrationList.as_view(),
        name="courseregistration_list",
    ),
    re_path(
        r"^user/registrations/cancel/(?P<pk>\d+)/?$",
        views.CancelCourseRegistration.as_view(),
        name="cancel_courseregistration",
    ),
    re_path(
        r"^user/registrations/update/(?P<pk>\d+)/?$",
        views.UpdateCourseRegistration.as_view(),
        name="update_courseregistration",
    ),
]
