import csv
import tempfile
import zipfile
from datetime import date

from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from parler.admin import TranslatableAdmin, TranslatableTabularInline

from course_registrations.models import CourseRegistration
from danbw_website import utils

from .models import AccommodationOption, CourseSession, ExternalCourse, InternalCourse


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


class CourseSessionInline(TranslatableTabularInline):
    """Displays CourseSessions as an inline model
    Django documentation for inline models:
    https://docs.djangoproject.com/en/4.2/ref/contrib/admin
    /#inlinemodeladmin-objects
    """

    model = CourseSession
    extra = 0  # Set number of additional rows to 0
    fields = ('title', 'date', 'start_time', 'end_time', 'is_dan_preparation')


class AccommodationOptionInline(TranslatableTabularInline):
    """Displays AccommodationOptions as an inline model"""

    model = AccommodationOption
    extra = 0  # Set number of additional rows to 0
    fields = ["name", "fee", "order"]


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
        "accommodation_option",
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
        "accommodation_option",
        "grade",
        "dojo",
    ]


@admin.register(InternalCourse)
class InternalCourseAdmin(TranslatableAdmin, SummernoteModelAdmin):
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
                "has_dinner"
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
                "bank_transfer_until",
                "dan_discount"
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
    inlines = [CourseSessionInline, AccommodationOptionInline, CourseRegistrationInline]
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
            while InternalCourse.objects.filter(translations__title=new_title).exists():
                new_title = f"Copy {counter} of {course.title}"
                counter += 1

            # Create new course with non-translated fields
            new_course = InternalCourse.objects.create(
                title=new_title,  # Will use current language
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
            )

            # Copy all translations
            from django.utils import translation as django_translation
            current_lang = django_translation.get_language()

            for trans in course.translations.all():
                if trans.language_code == current_lang:
                    # Update the existing translation created by .create(title=...)
                    existing_trans = new_course.translations.get(language_code=current_lang)
                    existing_trans.description = trans.description
                    existing_trans.location = trans.location
                    existing_trans.additional_info = trans.additional_info
                    existing_trans.save()
                else:
                    # Create translation for other languages
                    new_course.translations.create(
                        language_code=trans.language_code,
                        title=new_title,  # Use the new title
                        description=trans.description,
                        location=trans.location,
                        additional_info=trans.additional_info,
                    )

            # Copy sessions with translations
            for session in course.sessions.all():
                new_session = CourseSession.objects.create(
                    course=new_course,
                    date=session.date,
                    start_time=session.start_time,
                    end_time=session.end_time,
                )
                # Copy session translations
                for trans in session.translations.all():
                    new_session.translations.create(
                        language_code=trans.language_code,
                        title=trans.title,
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
class ExternalCourseAdmin(TranslatableAdmin, SummernoteModelAdmin):
    fields = (
        "title",
        "slug",
        "start_date",
        "end_date",
        "organizer",
        "teacher",
        "description",
        "location",
        "url",
    )

    list_display = (
        "title",
        "url",
        "start_date",
        "end_date",
    )

    readonly_fields = ("slug",)

    search_fields = ["translations__title", "translations__description"]
    summernote_fields = ("description",)
    actions = ["duplicate_selected_courses"]

    def duplicate_selected_courses(self, request, queryset):
        """Action for duplicating existing courses"""
        for course in queryset:
            new_title = f"Copy of {course.title}"
            counter = 2
            while ExternalCourse.objects.filter(translations__title=new_title).exists():
                new_title = f"Copy {counter} of {course.title}"
                counter += 1

            # Create new course with non-translated fields
            new_course = ExternalCourse.objects.create(
                title=new_title,  # Will use current language
                url=course.url,
                start_date=course.start_date,
                end_date=course.end_date,
                organizer=course.organizer,
                teacher=course.teacher,
            )

            # Copy all translations
            from django.utils import translation as django_translation
            current_lang = django_translation.get_language()

            for trans in course.translations.all():
                if trans.language_code == current_lang:
                    # Update the existing translation created by .create(title=...)
                    existing_trans = new_course.translations.get(language_code=current_lang)
                    existing_trans.description = trans.description
                    existing_trans.location = trans.location
                    existing_trans.additional_info = trans.additional_info
                    existing_trans.save()
                else:
                    # Create translation for other languages
                    new_course.translations.create(
                        language_code=trans.language_code,
                        title=new_title,  # Use the new title
                        description=trans.description,
                        location=trans.location,
                        additional_info=trans.additional_info,
                    )
