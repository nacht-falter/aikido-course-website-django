from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Course, CourseRegistration, CourseSession, UserProfile


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
        "user",
        "selected_sessions",
        "exam",
        "exam_passed",
        "accept_terms",
        "final_fee",
        "payment_status",
    ]
    readonly_fields = [
        "user",
        "selected_sessions",
        "exam",
        "accept_terms",
        "final_fee",
    ]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "registration_status",
        "description",
        "start_date",
        "end_date",
        "course_fee",
        "get_course_registration_count",
    )
    search_fields = ["title", "description"]
    list_filter = ("registration_status",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CourseSessionInline, CourseRegistrationInline]
    actions = [
        "duplicate_selected_courses",
        "toggle_registration_status",
    ]

    def duplicate_selected_courses(self, request, queryset):
        """Action for duplicating existing courses"""
        for course in queryset:
            new_title = f"Copy of {course.title}"
            new_slug = f"copy-of-{course.slug}"
            counter = 2
            while Course.objects.filter(title=new_title).exists():
                new_title = f"Copy {counter} of {course.title}"
                new_slug = f"copy-{counter}-of-{course.slug}"
                counter += 1

            Course.objects.create(
                title=new_title,
                slug=new_slug,
                description=course.description,
                registration_status=0,
                start_date=course.start_date,
                end_date=course.end_date,
                course_fee=course.course_fee,
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
        registrations = CourseRegistration.objects.filter(course=course)
        return len(registrations)

    # Customize property name: https://stackoverflow.com/a/64352815
    get_course_registration_count.short_description = "Registrations"


class UserProfileInline(admin.StackedInline):
    """Displays UserProfile as an inline model"""

    model = UserProfile
    extra = 0  # Set number of additional rows to 0
    fields = ["grade"]


# Add inlines to UserAdmin model: https://stackoverflow.com/a/35573797
UserAdmin.inlines += (UserProfileInline,)
