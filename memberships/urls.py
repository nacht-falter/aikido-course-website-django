from django.urls import re_path

from . import views

urlpatterns = [
    re_path(
        r"^membership/dan-international/?$",
        views.DanIntMembershipCreateView.as_view(),
        name="dan-international-membership"
    ),
    re_path(
        r"^membership/childrens-passport/?$",
        views.ChildrensPassportCreateView.as_view(),
        name="childrens-passport"
    ),
    re_path(
        r"^membership/danbw/?$",
        views.DanBwMembershipCreateView.as_view(),
        name="danbw-membership"
    ),
]
