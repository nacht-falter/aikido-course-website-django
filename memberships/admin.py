import csv
from datetime import date

from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import slugify
from django.utils.translation import gettext as _

from danbw_website import utils

from .models import ChildrensPassport, DanBwMembership, DanIntMembership


def toggle_passport_issued(modeladmin, request, queryset):
    for obj in queryset:
        obj.passport_issued = not obj.passport_issued
        obj.save()


toggle_passport_issued.short_description = _("Toggle Passport Status")


def export_csv(self, request, queryset):
    """Action for exporting course memberships to CSV"""

    membership_type = queryset.first().__class__.__name__.lower()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = (
        f"attachment; filename={membership_type}s_{slugify(date.today())}.csv"
    )
    writer = csv.writer(response)

    utils.write_membership_csv(writer, queryset)

    return response


export_csv.short_description = _("Export selected entries to CSV")


class BaseMembershipAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "dojo", "other_dojo"]
    readonly_fields = [
        "first_name",
        "last_name",
        "date_of_birth",
        "street",
        "street_number",
        "city",
        "postcode",
        "email",
        "phone_home",
        "phone_mobile",
        "grade",
        "dojo",
        "other_dojo",
        "accept_terms",
        "comment"
    ]
    actions = [toggle_passport_issued, export_csv]

    def has_add_permission(self, request):
        return "add" in request.path or "change" in request.path


@admin.register(DanIntMembership)
class DanIntMembershipAdmin(BaseMembershipAdmin):
    list_display = BaseMembershipAdmin.list_display + ["passport_issued"]
    readonly_fields = BaseMembershipAdmin.readonly_fields + [
        "liability_disclaimer",
        "sepa",
        "account_holder",
        "iban",
    ]


@admin.register(ChildrensPassport)
class ChildrensPassportAdmin(BaseMembershipAdmin):
    list_display = BaseMembershipAdmin.list_display + ["passport_issued"]
    readonly_fields = BaseMembershipAdmin.readonly_fields + [
        "name_legal_guardian",
        "liability_disclaimer",
    ]


@admin.register(DanBwMembership)
class DanBwMembershipAdmin(BaseMembershipAdmin):
    list_display = BaseMembershipAdmin.list_display
