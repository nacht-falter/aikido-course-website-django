from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Course, CourseRegistration
from .forms import CourseRegistrationForm


class CourseList(generic.ListView):
    """Displays a list of all courses"""

    model = Course
    queryset = Course.objects.all()
    template_name = "course_list.html"


class RegisterCourse(View):
    """Displays a registration form or a message"""

    def get(self, request, slug):
        courses = Course.objects.filter(registration_status=1)
        course = get_object_or_404(courses, slug=slug)
        user_registered = CourseRegistration.objects.filter(
            user=request.user, course=course
        )
        if user_registered:
            messages.warning(
                request, "You are already registered for this course."
            )
            return HttpResponseRedirect(reverse("course_list"))

        registration_form = CourseRegistrationForm()

        return render(
            request,
            "register_course.html",
            {"course": course, "form": registration_form},
        )

    def post(self, request, slug):
        queryset = Course.objects.filter(registration_status=1)
        course = get_object_or_404(queryset, slug=slug)
        registration_form = CourseRegistrationForm(data=request.POST)
        if registration_form.is_valid():
            registration = registration_form.save(commit=False)
            registration.course = course
            registration.user = request.user
            registration.save()
            messages.info(
                request, f"You have successfully signed up for {course.title}"
            )
        else:
            registration_form = CourseRegistrationForm()

        return HttpResponseRedirect(reverse("courseregistration_list"))


class CourseRegistrationList(generic.ListView):
    """Displays a list of a users course registrations"""

    model = CourseRegistration
    template_name = "courseregistration_list.html"
    # https://docs.djangoproject.com/en/3.2/topics/class-based-views/generic-display/#making-friendly-template-contexts
    context_object_name = "courseregistration_list"

    # https://stackoverflow.com/questions/24725617/how-to-make-generic-listview-only-show-users-listing
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
