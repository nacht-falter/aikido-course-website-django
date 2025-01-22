from django.contrib import admin

from fees.models import Fee


@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ["course_type", "fee_category", "fee_type",
                    "amount", "extra_fee_cash", "extra_fee_external"]

    ordering = ["course_type", "fee_type"]

    list_filter = ["course_type", "fee_type", "fee_category"]
