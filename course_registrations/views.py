from datetime import date

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.views import View

from courses.models import InternalCourse
from danbw_website.utils import send_registration_confirmation

from . import forms
from .models import (GuestCourseRegistration, UserCourseRegistration,
                     UserProfile)


class RegisterCourse(View):
    """Creates a course registration"""

    def prepare_course_data(self, course):
        """Prepares data to be passed to the template"""
        course_data = {"course_fee": course.course_fee,
                       "course_fee_cash": course.course_fee_cash,
                       "discount_percentage": course.discount_percentage
                       }
        counter = 0
        for session in course.sessions.all():
            course_data[f"session_{counter}_fee"] = session.session_fee
            course_data[f"session_{counter}_fee_cash"] = session.session_fee_cash
            counter += 1
        return course_data

    def get(self, request, slug):

        courses = InternalCourse.objects.filter(registration_status=1)
        course = get_object_or_404(courses, slug=slug)
        course_data = self.prepare_course_data(course)

        course.save()

        if course.registration_status == 0:
            messages.warning(
                request,
                "Registration for this course is not possible at the moment."
            )
            return HttpResponseRedirect(reverse("course_list"))

        if not request.user.is_authenticated and not request.GET.get("allow_guest"):
            return redirect('/accounts/login/?next=' + request.path + '&allow_guest=True')

        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user)
            if not user_profile:
                messages.warning(
                    request, "Please create a user profile to contine."
                )
                return redirect(reverse('userprofile') + '?next=' + request.path)

            user_registered = UserCourseRegistration.objects.filter(
                user=request.user, course=course
            )

            if user_registered:
                messages.warning(
                    request, "You are already registered for this course."
                )
                return HttpResponseRedirect(reverse("course_list"))

            registration_form = forms.UserCourseRegistrationForm(
                course=course, user_profile=request.user.profile
            )
        else:
            registration_form = forms.GuestCourseRegistrationForm(
                course=course
            )

        return render(
            request,
            "register_course.html",
            {
                "course": course,
                "form": registration_form,
                "course_data": course_data,
            },
        )

    def post(self, request, slug):
        queryset = InternalCourse.objects.filter(registration_status=1)
        course = get_object_or_404(queryset, slug=slug)
        course_data = self.prepare_course_data(course)

        if request.user.is_authenticated:
            registration_form = forms.UserCourseRegistrationForm(
                data=request.POST, course=course, user_profile=request.user.profile
            )
        else:
            registration_form = forms.GuestCourseRegistrationForm(
                data=request.POST, course=course
            )

        if registration_form.is_valid():
            if not request.user.is_authenticated:
                email = registration_form.cleaned_data.get("email")
                if GuestCourseRegistration.objects.filter(email=email, course=course).exists():
                    messages.warning(
                        request,
                        "A registration with this email address already exists."
                    )
                    return HttpResponseRedirect(reverse("course_list"))

            registration = registration_form.save(commit=False)
            registration.course = course

            selected_sessions = registration_form.cleaned_data.get(
                "selected_sessions"
            )

            registration.final_fee = registration.calculate_fees(
                course, selected_sessions
            )

            registration.dinner = registration_form.cleaned_data.get("dinner")

            if request.user.is_authenticated:
                registration.set_exam(request.user)
                registration.user = request.user
            else:
                registration.set_exam()
                registration.email = registration_form.cleaned_data.get(
                    "email")
                registration.first_name = registration_form.cleaned_data.get(
                    "first_name")
                registration.last_name = registration_form.cleaned_data.get(
                    "last_name")

            registration.save()

            # Update the registration to include the selected sessions.
            # Instructions on how to save objects with a many-
            # to-many field: https://docs.djangoproject.com/en/4.2/ref
            # /models/relations/#django.db.models.fields.related.Relat
            # edManager.set
            registration.selected_sessions.set(selected_sessions)

            send_registration_confirmation(
                request, registration
            )

            messages.info(
                request, f"You have successfully signed up for {course.title}"
            )
        else:
            if not registration_form.cleaned_data.get("selected_sessions"):
                messages.warning(
                    request,
                    "Registration not submitted. "
                    "Please select at least one session.",
                )

            if request.user.is_authenticated:
                registration_form = forms.UserCourseRegistrationForm(
                    course=course, user_profile=request.user.profile
                )
            else:
                registration_form = forms.GuestCourseRegistrationForm(
                    course=course
                )
            return render(
                request,
                "register_course.html",
                {
                    "course": course,
                    "form": registration_form,
                    "course_data": course_data,
                },
            )

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("courseregistration_list"))

        return HttpResponseRedirect(reverse("course_list"))


class UserCourseRegistrationList(LoginRequiredMixin, View):
    """Displays a list of a users course registrations"""

    def get(self, request):
        user_registrations = UserCourseRegistration.objects.filter(
            user=request.user
        )
        past_registrations = [
            registration
            for registration in user_registrations
            if registration.course.end_date < date.today()
        ]
        upcoming_registrations = [
            registration
            for registration in user_registrations
            if registration.course.end_date >= date.today()
        ]

        return render(
            request,
            "courseregistration_list.html",
            {
                "past_registrations": past_registrations,
                "upcoming_registrations": upcoming_registrations,
            },
        )


class CancelUserCourseRegistration(LoginRequiredMixin, SuccessMessageMixin, View):
    """Deletes a course registration instance"""

    def get(self, request, pk):
        registration = get_object_or_404(UserCourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied
        messages.warning(
            request,
            "Please cancel registrations by clicking the button from the "
            "'My Registrations' page.",
        )

        return HttpResponseRedirect(reverse("courseregistration_list"))

    def post(self, request, pk):
        registration = get_object_or_404(UserCourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        registration.delete()

        messages.success(
            request,
            f"Your registration for {registration.course.title} "
            "has been cancelled.",
        )
        return HttpResponseRedirect(reverse("courseregistration_list"))


class UpdateUserCourseRegistration(LoginRequiredMixin, View):
    """Updates a course registration"""

    def prepare_course_data(self, course):
        """Prepares data to be passed to the template"""
        course_data = {"course_fee": course.course_fee,
                       "course_fee_cash": course.course_fee_cash,
                       "discount_percentage": course.discount_percentage
                       }
        counter = 0
        for session in course.sessions.all():
            course_data[f"session_{counter}_fee"] = session.session_fee
            course_data[f"session_{counter}_fee_cash"] = session.session_fee_cash
            counter += 1
        return course_data

    def get(self, request, pk):
        registration = get_object_or_404(UserCourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        course = registration.course
        registration_form = forms.UserCourseRegistrationForm(
            instance=registration,
            course=course,
            user_profile=request.user.profile,
        )
        course_data = self.prepare_course_data(course)

        return render(
            request,
            "update_courseregistration.html",
            {
                "course": course,
                "form": registration_form,
                "course_data": course_data,
            },
        )

    def post(self, request, pk):
        registration = get_object_or_404(UserCourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        course = registration.course
        registration_form = forms.UserCourseRegistrationForm(
            data=request.POST,
            instance=registration,
            course=course,
            user_profile=request.user.profile,
        )

        course_data = self.prepare_course_data(course)

        if registration_form.is_valid():
            registration = registration_form.save(commit=False)

            selected_sessions = registration_form.cleaned_data.get(
                "selected_sessions"
            )

            registration.final_fee = registration.calculate_fees(
                course, selected_sessions
            )

            registration.set_exam(request.user)

            registration.save()

            # Update the registration to include the selected sessions.
            registration.selected_sessions.set(selected_sessions)

            messages.info(
                request,
                "You have successfully updated your registration for "
                f"{course.title}",
            )
        else:
            if not registration_form.cleaned_data.get("selected_sessions"):
                messages.warning(
                    request,
                    "Registration not submitted. "
                    "Please select at least one session.",
                )
            registration_form = forms.UserCourseRegistrationForm(
                instance=registration,
                course=course,
                user_profile=request.user.profile,
            )

            return render(
                request,
                "update_courseregistration.html",
                {
                    "course": course,
                    "form": registration_form,
                    "course_data": course_data,
                },
            )

        return HttpResponseRedirect(reverse("courseregistration_list"))
