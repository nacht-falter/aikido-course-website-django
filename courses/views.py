from django.shortcuts import render
from django.views import View

from .models import ExternalCourse, InternalCourse

from course_registrations.models import UserCourseRegistration

class CourseList(View):
    """Displays a list of all internal and external courses"""

    def get(self, request):
        all_courses = list(InternalCourse.objects.all()) + \
            list(ExternalCourse.objects.all())
        course_list = sorted(all_courses, key=lambda course: course.start_date)

        # Update the registration status for each course and set users registration status
        for course in course_list:
            course.save()

            if request.user.is_authenticated:
                course.user_registered = UserCourseRegistration.objects.filter(
                    user=request.user, course=course
                )

        return render(
            request,
            "course_list.html",
            {
                "course_list": course_list,
            },
        )
