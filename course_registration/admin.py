from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_summernote.admin import SummernoteModelAdmin
from django_summernote.widgets import SummernoteWidget
from django.db import models

from .models import (
    Course,
    CourseRegistration,
    CourseSession,
    UserProfile,
    Category,
    Page,
)


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
        "exam_grade",
        "exam_passed",
        "accept_terms",
        "final_fee",
        "payment_status",
    ]
    readonly_fields = [
        "user",
        "selected_sessions",
        "exam",
        "exam_grade",
        "accept_terms",
        "final_fee",
    ]


@admin.register(Course)
class CourseAdmin(SummernoteModelAdmin):
    list_display = (
        "title",
        "registration_status",
        "start_date",
        "end_date",
        "course_fee",
        "get_course_registration_count",
    )
    search_fields = ["title", "description"]
    list_filter = ("registration_status",)
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("description",)
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


@admin.register(Page)
class PageAdmin(SummernoteModelAdmin):
    list_display = ("title", "slug", "status", "category")
    search_fields = ["title", "content"]
    list_filter = ("status", "category")
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content",)


class PageInline(admin.StackedInline):
    """Displays pages as an inline model"""

    model = Page
    extra = 0
    fields = [
        "title",
        "slug",
        "category",
        "status",
        "featured_image",
        "content",
    ]
    # Add summernote field to inline model:
    # https://github.com/summernote/django-summernote/issues/14
    formfield_overrides = {models.TextField: {"widget": SummernoteWidget}}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title",)
    prepopulated_fields = {"slug": ("title",)}
    inlines = [PageInline]
