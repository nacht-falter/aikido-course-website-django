from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path(
        _("courses/register/<slug:slug>/"),
        views.RegisterCourse.as_view(),
        name="register_course",
    ),
    path(
        _("user/registrations/"),
        views.CourseRegistrationList.as_view(),
        name="courseregistration_list",
    ),
    path(
        _("user/registrations/cancel/<int:pk>/"),
        views.CancelCourseRegistration.as_view(),
        name="cancel_courseregistration",
    ),
    path(
        _("user/registrations/update/<int:pk>/"),
        views.UpdateCourseRegistration.as_view(),
        name="update_courseregistration",
    ),
    path(
        "export-csv/<slug:slug>/",
        views.ExportCourseRegistrations.as_view(),
        name="export_course_registrations",
    ),
    path(
        _("set-attendence-status/<int:pk>/"),
        views.SetRegistrationAttendenceStatus.as_view(),
        name="set_attendence_status",
    )
]
