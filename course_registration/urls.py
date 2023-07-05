from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.CourseList.as_view(), name="courses"),
    path(
        "courses/register/<slug:slug>/",
        views.RegisterCourse.as_view(),
        name="register_course",
    ),
]
