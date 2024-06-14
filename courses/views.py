from django.shortcuts import render
from django.views import View

from .models import ExternalCourse, InternalCourse

from course_registrations.models import UserCourseRegistration

class CourseList(View):
    """Displays a list of all internal and external courses"""

    def get(self, request):
        internal_courses = InternalCourse.objects.all()
        external_courses = ExternalCourse.objects.all()


        # Update the registration status for each course and set users registration status
        for course in internal_courses:
            course.save()

            if request.user.is_authenticated:
                course.user_registered = UserCourseRegistration.objects.filter(
                    user=request.user, course=course
                )

        all_courses = list(internal_courses) + list(external_courses)
        course_list = sorted(all_courses, key=lambda course: course.start_date)

        return render(
            request,
            "course_list.html",
            {
                "course_list": course_list,
            },
        )
