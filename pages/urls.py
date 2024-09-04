from django.urls import re_path

from . import views

urlpatterns = [
    re_path(r"^$", views.HomePage.as_view(), name="home"),
    re_path(r"^contact/?$", views.ContactPage.as_view(), name="contact"),
    re_path(r"^category/(?P<category_slug>[\w-]+)/?$",
            views.PageList.as_view(), name="page_list"),
    re_path(r"^(?P<slug>[\w-]+)/?$",
            views.PageDetail.as_view(), name="page_detail"),
    re_path(r'^.*$', views.catch_all_404_view, name='catch-all'),
]
