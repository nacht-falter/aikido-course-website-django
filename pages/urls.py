from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), name="home"),
    path(_("contact/"), views.ContactPage.as_view(), name="contact"),
    path(
        _("category/<slug:category_slug>/"),
        views.PageList.as_view(),
        name="page_list",
    ),
    path(
        "<slug:slug>/",
        views.PageDetail.as_view(),
        name="page_detail",
    ),
]
