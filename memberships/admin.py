from django.contrib import admin

from .models import DanIntMembership


@admin.register(DanIntMembership)
class DanIntMembershipAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "dojo"]

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return ("add" in request.path or "change" in request.path)
