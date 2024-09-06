from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path(_("membership/dan-international/"), views.DanIntMembershipCreateView.as_view(),
         name="dan-international-membership"),
    path(_("membership/childrens-passport/"), views.ChildrensPassportCreateView.as_view(),
         name="childrens-passport"),
    path(_("membership/danbw/"), views.DanBwMembershipCreateView.as_view(),
         name="danbw-membership"),
]
