from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_prose_editor.widgets import AdminProseEditorWidget
from parler.admin import TranslatableAdmin, TranslatableStackedInline

from .models import Category, Page


@admin.register(Page)
class PageAdmin(TranslatableAdmin):
    fields = ("title", "slug", "category", "status", "featured_image", "content", "menu_position")
    readonly_fields = ("slug",)
    list_display = ("title", "slug", "status", "category")
    search_fields = ["translations__title", "translations__content"]
    list_filter = ("status", "category")
    actions = ["toggle_status"]

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "content":
            kwargs["widget"] = AdminProseEditorWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)

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

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == "content":
            kwargs["widget"] = AdminProseEditorWidget
        return super().formfield_for_dbfield(db_field, request, **kwargs)


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    fields = ("title", "slug", "menu_position")
    readonly_fields = ("slug",)
    list_display = ("title",)
    search_fields = ["translations__title"]
    inlines = [PageInline]
