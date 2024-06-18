from datetime import date

from django.shortcuts import render
from django.views import View

from course_registrations.models import UserCourseRegistration

from .models import ExternalCourse, InternalCourse


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
        all_courses = sorted(
            all_courses, key=lambda course: course.start_date, reverse=True)
        past_courses = filter(
            lambda course: course.start_date < date.today(), all_courses)
        current_courses = filter(
            lambda course: course.start_date >= date.today(), all_courses)

        return render(
            request,
            "course_list.html",
            {
                "past_courses": past_courses,
                "current_courses": current_courses,
            },
        )
