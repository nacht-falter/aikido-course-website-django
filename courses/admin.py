import csv
import tempfile
import zipfile

from django.contrib import admin
from django.http import HttpResponse
from django.utils.text import slugify
from django_summernote.admin import SummernoteModelAdmin

from course_registrations.models import (GuestCourseRegistration,
                                         UserCourseRegistration)

from .models import CourseSession, ExternalCourse, InternalCourse


class CourseSessionInline(admin.TabularInline):
    """Displays CourseSessions as an inline model
    Django documentation for inline models:
    https://docs.djangoproject.com/en/4.2/ref/contrib/admin
    /#inlinemodeladmin-objects
    """

    model = CourseSession
    extra = 0  # Set number of additional rows to 0


class UserCourseRegistrationInline(admin.TabularInline):
    """Displays UserCourseRegistrations as an inline model"""

    model = UserCourseRegistration
    extra = 0  # Set number of additional rows to 0
    max_num = 0  # Hide option to add more rows
    fields = [
        "user",
        "selected_sessions",
        "exam",
        "exam_grade",
        "exam_passed",
        "accept_terms",
        "final_fee",
        "payment_status",
        "payment_method",
        "discount",
        "dinner",
    ]
    readonly_fields = [
        "user",
        "selected_sessions",
        "exam",
        "exam_grade",
        "accept_terms",
        "final_fee",
        "payment_method",
        "discount",
        "dinner",
    ]


class GuestCourseRegistrationInline(admin.TabularInline):
    """Displays GuestCourseRegistrations as an inline model"""

    model = GuestCourseRegistration
    extra = 0  # Set number of additional rows to 0
    max_num = 0  # Hide option to add more rows
    fields = [
        "email",
        "first_name",
        "last_name",
        "selected_sessions",
        "exam",
        "exam_grade",
        "accept_terms",
        "final_fee",
        "payment_status",
        "payment_method",
        "discount",
        "dinner",
    ]
    readonly_fields = [
        "email",
        "first_name",
        "last_name",
        "selected_sessions",
        "exam",
        "exam_grade",
        "accept_terms",
        "final_fee",
        "payment_method",
        "discount",
        "dinner",
    ]


@admin.register(InternalCourse)
class InternalCourseAdmin(SummernoteModelAdmin):
    fields = (
        "title",
        "start_date",
        "end_date",
        "registration_status",
        "registration_start_date",
        "registration_end_date",
        "organizer",
        "teacher",
        "course_fee",
        "course_fee_cash",
        "discount_percentage",
        "bank_transfer_until",
        "dinner",
        "description",
    )
    list_display = (
        "title",
        "registration_status",
        "start_date",
        "end_date",
        "course_fee",
        "course_fee_cash",
        "get_course_registration_count",
    )
    search_fields = ["title", "description"]
    list_filter = ("registration_status",)
    summernote_fields = ("description",)
    inlines = [CourseSessionInline, UserCourseRegistrationInline,
               GuestCourseRegistrationInline]
    actions = [
        "duplicate_selected_courses",
        "toggle_registration_status",
        "export_csv"
    ]

    def duplicate_selected_courses(self, request, queryset):
        """Action for duplicating existing courses"""
        for course in queryset:
            new_title = f"Copy of {course.title}"
            new_slug = f"copy-of-{course.slug}"
            counter = 2
            while InternalCourse.objects.filter(title=new_title).exists():
                new_title = f"Copy {counter} of {course.title}"
                new_slug = f"copy-{counter}-of-{course.slug}"
                counter += 1

            InternalCourse.objects.create(
                title=new_title,
                slug=new_slug,
                description=course.description,
                registration_status=0,
                start_date=course.start_date,
                end_date=course.end_date,
                registration_start_date=course.registration_start_date,
                registration_end_date=course.registration_end_date,
                course_fee=course.course_fee,
                course_fee_cash=course.course_fee_cash,
                organizer=course.organizer,
                teacher=course.teacher,
                discount_percentage=course.discount_percentage,
                bank_transfer_until=course.bank_transfer_until,
                dinner=course.dinner,
            )

            for session in course.sessions.all():
                CourseSession.objects.create(
                    title=session.title,
                    course=InternalCourse.objects.get(title=new_title),
                    date=session.date,
                    start_time=session.start_time,
                    end_time=session.end_time,
                    session_fee=session.session_fee,
                )

    def toggle_registration_status(self, request, queryset):
        """Action for toggling course registration status"""
        for course in queryset:
            if course.registration_status == 0:
                course.registration_status = 1
            else:
                course.registration_status = 0
            course.save()

    toggle_registration_status.short_description = (
        "Toggle registration status of selected courses"
    )

    def get_course_registration_count(self, course):
        """Gets the number of registrations for a course"""

        registrations = list(
            UserCourseRegistration.objects.filter(course=course))
        registrations += list(
            GuestCourseRegistration.objects.filter(course=course))

        return len(registrations)

    def write_csv_data(self, writer, registrations):
        """Write registration data to CSV"""

        # Write header row
        header_row = [
            "First Name",
            "Last Name",
            "Email",
            "Grade",
            "Selected Sessions",
            "Exam",
            "Exam Grade",
            "Accept Terms",
            "Final Fee",
            "Payment Status"
        ]
        if registrations and registrations[0].course.dinner:
            header_row.append("Dinner")
        writer.writerow(header_row)

        # Write data rows
        for registration in registrations:
            selected_sessions = ", ".join(
                session.title for session in registration.selected_sessions.all())

            if hasattr(registration, 'user'):
                user = registration.user
            else:
                user = None

            data_row = [
                user.first_name if user else registration.first_name,
                user.last_name if user else registration.last_name,
                user.email if user else registration.email,
                user.profile.get_grade_display() if user else registration.get_grade_display(),
                selected_sessions,
                "Yes" if registration.exam else "No",
                registration.get_exam_grade_display(),
                "Yes" if registration.accept_terms else "No",
                registration.final_fee,
                registration.get_payment_status_display(),
            ]
            if registration.course.dinner:
                data_row.append("Yes" if registration.dinner else "No")
            writer.writerow(data_row)

    def export_csv(self, request, queryset):
        """Action for exporting course registrations to CSV or zip"""

        if queryset.count() == 1:
            course = queryset.first()
            response = HttpResponse(content_type="text/csv")
            response["Content-Disposition"] = (
                f"attachment; filename={slugify(course.title)}_registrations.csv"
            )
            writer = csv.writer(response)

            registrations = list(
                UserCourseRegistration.objects.filter(course=course))
            registrations += list(
                GuestCourseRegistration.objects.filter(course=course))

            self.write_csv_data(writer, registrations)

            return response

        zip_buffer = tempfile.TemporaryFile()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for course in queryset:
                csv_filename = f"{slugify(course.title)}_registrations.csv"

                registrations = list(
                    UserCourseRegistration.objects.filter(course=course))
                registrations += list(
                    GuestCourseRegistration.objects.filter(course=course))

                with tempfile.NamedTemporaryFile(
                    delete=False, mode='w', newline=''
                ) as csv_file:
                    writer = csv.writer(csv_file)
                    self.write_csv_data(
                        writer, registrations)
                zip_file.write(csv_file.name, arcname=csv_filename)
        zip_buffer.seek(0)

        response = HttpResponse(
            zip_buffer.read(), content_type='application/zip')
        response['Content-Disposition'] = (
            'attachment; filename=courses_registrations.zip'
        )

        return response

    # Customize property name: https://stackoverflow.com/a/64352815
    get_course_registration_count.short_description = "Registrations"


@admin.register(ExternalCourse)
class ExternalCourseAdmin(SummernoteModelAdmin):
    fields = (
        "title",
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
    search_fields = ["title", "description"]
    summernote_fields = ("description",)
    actions = ["duplicate_selected_courses"]

    def duplicate_selected_courses(self, request, queryset):
        """Action for duplicating existing courses"""
        for course in queryset:
            new_title = f"Copy of {course.title}"
            new_slug = f"copy-of-{course.slug}"
            counter = 2
            while ExternalCourse.objects.filter(title=new_title).exists():
                new_title = f"Copy {counter} of {course.title}"
                new_slug = f"copy-{counter}-of-{course.slug}"
                counter += 1
            ExternalCourse.objects.create(
                title=new_title,
                slug=new_slug,
                url=course.url,
                start_date=course.start_date,
                end_date=course.end_date,
                organizer=course.organizer,
                teacher=course.teacher,
            )
