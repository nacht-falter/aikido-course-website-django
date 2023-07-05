from django.urls import path
from . import views

urlpatterns = [
    path("courses/", views.CourseList.as_view(), name="courses"),
]
