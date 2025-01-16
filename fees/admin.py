from django.contrib import admin

from fees.models import Fee

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ["course_type", "fee_type", "fee_category", "dan_discount", "payment_method", "amount"]
