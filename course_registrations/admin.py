import csv
from datetime import date

from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from danbw_website import utils

from .models import CourseRegistration


class FutureCourseFilter(admin.SimpleListFilter):
    """Filter for future and past courses
    https://docs.djangoproject.com/en/5.0/ref/contrib/admin/filters/
    """

    title = _("Course Date")
    parameter_name = "future_course"

    def lookups(self, request, model_admin):
        return (
            ("future", _("Future Courses")),
            ("past", _("Past Courses")),
        )

    def queryset(self, request, queryset):
        if self.value() == "future":
            return queryset.filter(course__start_date__gte=date.today())
        elif self.value() == "past":
            return queryset.filter(course__start_date__lt=date.today())


class CourseFilter(admin.SimpleListFilter):
    """Filter for courses
    https://docs.djangoproject.com/en/5.0/ref/contrib/admin/filters/
    """
    title = _("Course")
    parameter_name = "course"

    def lookups(self, request, model_admin):
        courses = CourseRegistration.objects.values_list(
            "course__title", flat=True).distinct()
        return tuple((course, course) for course in courses)

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(course__title=self.value())
        return queryset


@admin.register(CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "registration_str",
        "course",
        "email",
        "exam",
        "exam_grade",
        "final_fee",
        "payment_status",
        "payment_method",
        "discount",
        "dinner",
        "overnight_stay"
    ]
    fields = [
        "course",
        "first_name",
        "last_name",
        "email",
        "selected_sessions",
        "exam",
        "exam_grade",
        "accept_terms",
        "final_fee",
        "payment_status",
        "payment_method",
        "discount",
        "dinner",
        "overnight_stay"
    ]
    readonly_fields = [
        "course",
        "first_name",
        "last_name",
        "email",
        "selected_sessions",
        "exam",
        "exam_grade",
        "accept_terms",
        "final_fee",
        "payment_method",
        "discount",
        "dinner",
        "overnight_stay"
    ]
    search_fields = ["course__title", "first_name", "last_name", "email"]
    list_filter = [FutureCourseFilter, CourseFilter, "payment_status",
                   "payment_method", "exam"]
    ordering = ["course__start_date", "-registration_date"]
    actions = [
        "toggle_payment_status", "export_csv"
    ]

    def get_list_display_links(self, request, list_display):
        return ["registration_str"]

    def registration_str(self, obj):
        return str(obj)
    registration_str.short_description = _("Registration")

    def has_add_permission(self, request):
        return ("add" in request.path or "change" in request.path)

    def toggle_payment_status(self, request, queryset):
        """Action for toggling the payment status of registrations"""
        for registration in queryset:
            registration.payment_status = not registration.payment_status
            registration.save()

    toggle_payment_status.short_description = _(
        "Toggle payment status of selected registrations"
    )

    def export_csv(self, request, queryset):
        """Action for exporting course registrations to CSV"""

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = (
            f"attachment; filename={_('registrations')}_{slugify(date.today())}.csv"
        )
        writer = csv.writer(response)

        utils.write_registrations_csv(writer, queryset)

        return response

    export_csv.short_description = _("Export selected course registrations to CSV")
