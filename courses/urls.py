from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^courses/?$", views.CourseList.as_view(), name="course_list"),
]
