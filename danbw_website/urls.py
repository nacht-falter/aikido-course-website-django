"""danbw_website URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.templatetags.static import static as static_url
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path('captcha/', include('captcha.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt", content_type="text/plain"
        ),
    ),
]

# Devices and crawlers request these at the site root regardless of the
# icon links in base.html
apple_touch_icon = RedirectView.as_view(
    url=static_url("favicon/apple-touch-icon.png"), permanent=True
)
urlpatterns += [
    path(f"{name}.png", apple_touch_icon)
    for name in [
        "apple-touch-icon",
        "apple-touch-icon-precomposed",
        "apple-touch-icon-120x120",
        "apple-touch-icon-120x120-precomposed",
    ]
]

urlpatterns += i18n_patterns(
    path("", include("users.urls")),
    path("", include("courses.urls")),
    path("", include("course_registrations.urls")),
    path("", include("memberships.urls")),
    path("", include("pages.urls")),
)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
