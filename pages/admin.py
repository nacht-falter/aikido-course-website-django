from django.contrib import admin
from django.db import models
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from django.utils.translation import gettext_lazy as _

from .models import Category, Page


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    list_display = ("title", "slug", "status", "category")
    search_fields = ["title", "content"]
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("status", "category")
    summernote_fields = ("content",)
    actions = ["toggle_status"]

    def toggle_status(self, request, queryset):
        """Action for toggling page status"""
        for page in queryset:
            if page.status == 0:
                page.status = 1
            else:
                page.status = 0
            page.save()

    toggle_status.short_description = _("Toggle page status")


class PageInline(admin.StackedInline):
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
    ]
    prepopulated_fields = {"slug": ("title",)}
    # Add summernote field to inline model:
    # https://github.com/summernote/django-summernote/issues/14
    formfield_overrides = {models.TextField: {"widget": SummernoteWidget}}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ("title", "slug", "menu_position")
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageInline]
