from django.shortcuts import render
from django.views import View

from .models import ExternalCourse, InternalCourse


class CourseList(View):
    """Displays a list of all internal and external courses"""

    def get(self, request):
        all_courses = list(InternalCourse.objects.all()) + \
            list(ExternalCourse.objects.all())
        course_list = sorted(all_courses, key=lambda course: course.start_date)

        # Update the registration status for each course
        for course in course_list:
            course.save()

        return render(
            request,
            "course_list.html",
            {
                "course_list": course_list,
            },
        )
