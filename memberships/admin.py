from django.contrib import admin

from .models import ChildrensPassport, DanIntMembership


@admin.register(DanIntMembership)
class DanIntMembershipAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "dojo", "passport_issued"]
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
        "liability_disclaimer",
        "comment",
        "sepa",
        "account_holder",
        "iban"
    ]

    def has_add_permission(self, request):
        return ("add" in request.path or "change" in request.path)


@admin.register(ChildrensPassport)
class ChildrensPassportAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "email", "dojo", "passport_issued"]
    readonly_fields = [
        "first_name",
        "last_name",
        "date_of_birth",
        "street",
        "street_number",
        "city",
        "postcode",
        "name_legal_guardian",
        "email",
        "phone_home",
        "phone_mobile",
        "grade",
        "dojo",
        "other_dojo",
        "accept_terms",
        "liability_disclaimer",
        "comment",
    ]

    def has_add_permission(self, request):
        return ("add" in request.path or "change" in request.path)

def toggle_passport_issued(modeladmin, request, queryset):
    for obj in queryset:
        obj.passport_issued = not obj.passport_issued
        obj.save()
