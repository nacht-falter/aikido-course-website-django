from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path(
        "pages/<slug:category_slug>/",
        views.PageList.as_view(),
        name="page_list",
    ),
    path("contact/", views.ContactPage.as_view(), name="contact"),
]
