from django.contrib import admin
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin, TranslatableStackedInline

from .models import Category, Page


@admin.register(Page)
class PageAdmin(TranslatableAdmin, SummernoteModelAdmin):
    fields = ("title", "slug", "category", "status", "featured_image", "content", "menu_position")
    readonly_fields = ("slug",)
    list_display = ("title", "slug", "status", "category")
    search_fields = ["translations__title", "translations__content"]
    list_filter = ("status", "category")
    summernote_fields = ("content",)
    actions = ["toggle_status"]

    def toggle_status(self, request, queryset):
        """Action for toggling page status"""
        for page in queryset:
            page.status = not page.status
            page.save()

    toggle_status.short_description = _("Toggle page status")


class PageInline(TranslatableStackedInline):
    """Displays pages as an inline model"""

    model = Page
    extra = 0
    fields = [
        "title",
        "slug",
        "category",
        "status",
        "featured_image",
        "content",
        "menu_position"
    ]
    readonly_fields = ["slug"]
    summernote_fields = ('content',)
    # Add summernote field to inline model:
    # https://github.com/summernote/django-summernote/issues/14
    formfield_overrides = {models.TextField: {"widget": SummernoteWidget}}


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    fields = ("title", "slug", "menu_position")
    readonly_fields = ("slug",)
    list_display = ("title",)
    search_fields = ["translations__title"]
    inlines = [PageInline]
