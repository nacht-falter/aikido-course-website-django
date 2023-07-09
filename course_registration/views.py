from datetime import date

from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .models import Course, CourseRegistration, UserProfile
from .forms import CourseRegistrationForm, UserProfileForm

CURRENT_DATE = date.today()


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


class CourseRegistrationList(View):
    """Displays a list of a users course registrations"""

    def get(self, request):
        user_registrations = CourseRegistration.objects.filter(
            user=request.user
        )
        current_date = date.today()
        past_registrations = [
            registration
            for registration in user_registrations
            if registration.course.end_date < current_date
        ]
        upcoming_registrations = [
            registration
            for registration in user_registrations
            if registration.course.end_date > current_date
        ]

        return render(
            request,
            "courseregistration_list.html",
            {
                "past_registrations": past_registrations,
                "upcoming_registrations": upcoming_registrations,
            },
        )


class CancelCourseRegistration(SuccessMessageMixin, generic.edit.DeleteView):
    """Deletes a course registration instance
    Documentation for DeleteView:
    https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic
    -editing/#deleteview
    """

    model = CourseRegistration
    success_url = reverse_lazy("courseregistration_list")
    template_name = "courseregistration_confirm_delete.html"

    # Get success message:
    # https://stackoverflow.com/questions/74756918/django-deleteview-
    # successmessagemixin-how-to-pass-data-to-message
    def get_success_message(self, cleaned_data):
        return (
            f"Your registration for {self.object.course.title}"
            " has been cancelled."
        )


class UpdateCourseRegistration(SuccessMessageMixin, generic.edit.UpdateView):
    """Updates a course registration instance
    Documentation for UpdateView:
    https://docs.djangoproject.com/en/3.2/ref/class-based-views/generic
    -editing/#updateview
    """

    model = CourseRegistration
    fields = [
        "exam",
        "accept_terms",
        "final_fee",
    ]
    success_url = reverse_lazy("courseregistration_list")
    template_name = "courseregistration_update.html"

    # Get success message:
    # https://stackoverflow.com/questions/74756918/django-deleteview-
    # successmessagemixin-how-to-pass-data-to-message
    def get_success_message(self, cleaned_data):
        return (
            f"Your registration for {self.object.course.title}"
            " has been updated."
        )


class UserProfileView(LoginRequiredMixin, View):
    """Displays a user profile or a form to create a new profile.
    Documentation for LoginRequiredMixin: https://docs.djangoproject
    .com/en/4.2/topics/auth/default/#the-loginrequiredmixin-mixin
    """

    def get(self, request):
        user = request.user
        profiles = UserProfile.objects.filter(user=user)
        if profiles:
            profile = get_object_or_404(profiles, user=user)
            return render(request, "userprofile.html", {"profile": profile})

        else:
            profile_form = UserProfileForm()
            return render(
                request,
                "create_userprofile.html",
                {"form": profile_form},
            )

    def post(self, request):
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            UserProfile.objects.create(
                user=request.user,
                grade=profile_form.cleaned_data["grade"],
                first_name=profile_form.cleaned_data["first_name"],
                last_name=profile_form.cleaned_data["last_name"],
            )
            messages.info(
                request, "You have successfully created a user profile."
            )
        else:
            profile_form = UserProfileForm()

        return HttpResponseRedirect(reverse("userprofile"))
