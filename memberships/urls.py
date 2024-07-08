from django.urls import path

from . import views

urlpatterns = [
    path("membership/dan-international/", views.DanIntMembershipCreateView.as_view(),
         name="dan-international-membership"),
    path("membership/childrens-passport/", views.ChildrensPassportCreateView.as_view(),
         name="childrens-passport"),
    path("membership/danbw/", views.DanBwMembershipCreateView.as_view(),
         name="danbw-membership"),
    path("membership/", views.MembershipPage.as_view(), name="membership"),
]
