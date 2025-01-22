import csv
import tempfile
import zipfile
from datetime import date

from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin

from course_registrations.models import CourseRegistration
from danbw_website import utils

from .models import CourseSession, ExternalCourse, InternalCourse


class CoursesByYearFilter(admin.SimpleListFilter):
    """Filter for displaying courses by year"""

    title = _("Year")
    parameter_name = "year"

    def lookups(self, request, model_admin):
        years = InternalCourse.objects.dates("start_date", "year")
        return [(year.year, year.year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(start_date__year=self.value())
        return queryset


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
            return queryset.filter(start_date__gte=date.today())
        elif self.value() == "past":
            return queryset.filter(start_date__lt=date.today())


class CourseSessionInline(admin.TabularInline):
    """Displays CourseSessions as an inline model
    Django documentation for inline models:
    https://docs.djangoproject.com/en/4.2/ref/contrib/admin
    /#inlinemodeladmin-objects
    """

    model = CourseSession
    extra = 0  # Set number of additional rows to 0


class CourseRegistrationInline(admin.TabularInline):
    """Displays CourseRegistrations as an inline model"""

    model = CourseRegistration
    extra = 0  # Set number of additional rows to 0
    max_num = 0  # Hide option to add more rows
    fields = [
        "first_name",
        "last_name",
        "email",
        "grade",
        "dojo",
        "truncated_session_display",
        "final_fee",
        "payment_status",
        "payment_method",
        "discount",
        "exam",
        "truncated_comment",
        "accept_terms",
        "dinner",
        "overnight_stay",
    ]
    readonly_fields = [
        "first_name",
        "last_name",
        "email",
        "truncated_session_display",
        "exam",
        "accept_terms",
        "final_fee",
        "payment_method",
        "discount",
        "truncated_comment",
        "dinner",
        "overnight_stay",
        "grade",
        "dojo",
    ]


@admin.register(InternalCourse)
class InternalCourseAdmin(SummernoteModelAdmin):
    fieldsets = (
        (_("Course Details"), {
            "fields": (
                "title",
                "slug",
                "course_type",
                "fee_category",
                "status",
                "publication_date",
                "organizer",
                "teacher",
                "description",
                "flyer",
                "location",
                "dan_discount",
            )
        }),
        (_("Dates"), {
            "fields": (
                "start_date",
                "end_date",
                "registration_status",
                "registration_start_date",
                "registration_end_date"
            )
        }),
        (_("Payment Information"), {
            "fields": (
                "discount_percentage",
                "bank_transfer_until"
            )
        }),
        (_("Additional Information"), {
            "fields": (
                "additional_info",
            )
        }),
    )

    readonly_fields = ("slug",)

    list_display = (
        "title",
        "status",
        "publication_date",
        "registration_status",
        "start_date",
        "end_date",
        "get_course_registration_count",
    )
    search_fields = ["title", "description"]
    list_filter = (CoursesByYearFilter, FutureCourseFilter,
                   "course_type", "status", "registration_status")
    summernote_fields = ("description",)
    inlines = [CourseSessionInline, CourseRegistrationInline]
    ordering = ["-start_date"]
    actions = [
        "duplicate_selected_courses",
        "toggle_status",
        "toggle_registration_status",
        "export_csv"
    ]

    def duplicate_selected_courses(self, request, queryset):
        """Action for duplicating existing courses"""
        for course in queryset:
            new_title = f"Copy of {course.title}"
            counter = 2
            while InternalCourse.objects.filter(title=new_title).exists():
                new_title = f"Copy {counter} of {course.title}"
                counter += 1

            new_course = InternalCourse.objects.create(
                title=new_title,
                description=course.description,
                registration_status=0,
                start_date=course.start_date,
                end_date=course.end_date,
                registration_start_date=course.registration_start_date,
                registration_end_date=course.registration_end_date,
                organizer=course.organizer,
                teacher=course.teacher,
                discount_percentage=course.discount_percentage,
                bank_transfer_until=course.bank_transfer_until,
                course_type=course.course_type,
                fee_category=course.fee_category,
                additional_info=course.additional_info,
            )

            for session in course.sessions.all():
                CourseSession.objects.create(
                    title=session.title,
                    course=new_course,
                    date=session.date,
                    start_time=session.start_time,
                    end_time=session.end_time,
                )

    duplicate_selected_courses.short_description = _(
        "Duplicate selected courses")

    def toggle_registration_status(self, request, queryset):
        """Action for toggling course registration status"""
        for course in queryset:
            course.registration_status = not course.registration_status
            course.save()

    toggle_registration_status.short_description = _(
        "Toggle registration status of selected courses")

    def toggle_status(self, request, queryset):
        """Action for toggling course status"""
        for course in queryset:
            course.status = not course.status
            course.save()

    toggle_status.short_description = _("Toggle status of selected courses")

    def get_course_registration_count(self, course):
        """Gets the number of registrations for a course"""

        registrations = CourseRegistration.objects.filter(course=course)

        return len(registrations)

    # Customize property name: https://stackoverflow.com/a/64352815
    get_course_registration_count.short_description = _("Registrations")

    def export_csv(self, request, queryset):
        """Action for exporting course registrations to CSV or zip"""

        if queryset.count() == 1:
            course = queryset.first()
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                f"attachment; filename={slugify(course.title)}_{_('registrations')}.csv"
            )
            writer = csv.writer(response)

            registrations = CourseRegistration.objects.filter(course=course)

            utils.write_registrations_csv(writer, registrations)

            return response

        zip_buffer = tempfile.TemporaryFile()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for course in queryset:
                csv_filename = f"{slugify(course.title)}_{_('registrations')}.csv"

                registrations = CourseRegistration.objects.filter(
                    course=course)

                with tempfile.NamedTemporaryFile(
                    delete=False, mode="w", newline=""
                ) as csv_file:
                    writer = csv.writer(csv_file)
                    utils.write_registrations_csv(
                        writer, registrations)
                zip_file.write(csv_file.name, arcname=csv_filename)
        zip_buffer.seek(0)

        response = HttpResponse(
            zip_buffer.read(), content_type="application/zip")
        response["Content-Disposition"] = (
            f"attachment; filename={slugify(_('course_registrations'))}_{slugify(date.today())}.zip"
        )

        return response

    export_csv.short_description = _(
        "Export selected course registrations to CSV")


@admin.register(ExternalCourse)
class ExternalCourseAdmin(SummernoteModelAdmin):
    fields = (
        "title",
        "slug",
        "start_date",
        "end_date",
        "organizer",
        "teacher",
        "url",
    )

    list_display = (
        "title",
        "url",
        "start_date",
        "end_date",
    )

    readonly_fields = ("slug",)

    search_fields = ["title", "description"]
    summernote_fields = ("description",)
    actions = ["duplicate_selected_courses"]

    def duplicate_selected_courses(self, request, queryset):
        """Action for duplicating existing courses"""
        for course in queryset:
            new_title = f"Copy of {course.title}"
            counter = 2
            while ExternalCourse.objects.filter(title=new_title).exists():
                new_title = f"Copy {counter} of {course.title}"
                counter += 1
            ExternalCourse.objects.create(
                title=new_title,
                url=course.url,
                start_date=course.start_date,
                end_date=course.end_date,
                organizer=course.organizer,
                teacher=course.teacher,
            )
