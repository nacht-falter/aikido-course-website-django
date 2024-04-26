from django.urls import path

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
    path(
        "pages/<slug:category_slug>/",
        views.PageList.as_view(),
        name="page_list",
    ),
    path("contact/", views.ContactPage.as_view(), name="contact"),
]
