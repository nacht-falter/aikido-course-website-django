from django.urls import path
from . import views

urlpatterns = [
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
]
