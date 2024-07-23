from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path("contact/", views.ContactPage.as_view(), name="contact"),
    path(
        "<slug:slug>/",
        views.PageDetail.as_view(),
        name="page_detail",
    ),
]
