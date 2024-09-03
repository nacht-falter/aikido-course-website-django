from django.urls import resolve
from django.utils.translation import gettext as _

from .models import Category


def add_categories_to_context(request):
    """Context processor to pass categories to templates
    Adapted from: https://stackoverflow.com/a/34903331
    Django documentation for context processors:
    https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-
    your-own-context-processors
    """
    categories = Category.objects.exclude(slug="footer-links")

    try:
        footer_links = Category.objects.get(slug="footer-links")
    except Category.DoesNotExist:
        footer_links = None

    return {"categories": categories, "footer_links": footer_links, "category_slug": None, "page_slug": None}


def breadcrumb_context(request):
    url_name = resolve(request.path_info).url_name

    page_name = ""

    if url_name == "userprofile":
        page_name = _("My Profile")
    elif url_name == "courseregistration_list":
        page_name = _("My Registrations")
    elif url_name == "course_list":
        page_name = _("Courses")
    elif url_name == "contact":
        page_name = _("Contact us")

    return {"page_name": page_name}
