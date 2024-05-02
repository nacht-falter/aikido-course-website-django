from django.urls import path

from . import views

urlpatterns = [
    path('membership/application/', views.DanIntMembershipCreateView.as_view(),
        name='membership_application'),
]
