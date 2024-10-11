import csv
import os
from datetime import date
from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render, reverse)
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.views import View

from courses.models import InternalCourse
from danbw_website import utils

from . import forms
from .models import CourseRegistration, UserProfile


class RegisterCourse(View):
    """Creates a course registration"""

    def prepare_course_data(self, course):
        """Prepares data to be passed to the template"""
        course_data = {"course_fee": course.course_fee,
                       "course_fee_cash": course.course_fee_cash,
                       "course_fee_with_dan_preparation": course.course_fee_with_dan_preparation,
                       "course_fee_with_dan_preparation_cash": course.course_fee_with_dan_preparation_cash,
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
                _("Registration for this course is not possible at the moment.")
            )
            return HttpResponseRedirect(reverse("course_list"))

        if not request.user.is_authenticated and not request.GET.get("allow_guest"):
            messages.info(
                request,
                _("Please log in to your account or continue as a guest.")
            )
            return redirect('/accounts/login/?next=' + request.path + '&allow_guest=True')

        if request.user.is_authenticated:
            user_profile = UserProfile.objects.filter(user=request.user)
            if not user_profile:
                messages.warning(
                    request,
                    _("Please create a user profile to contine.")
                )
                return redirect(reverse('userprofile') + '?next=' + request.path)

            user_registered = CourseRegistration.objects.filter(
                user=request.user, course=course
            )

            if user_registered:
                messages.warning(
                    request,
                    _("You are already registered for this course.")
                )
                return HttpResponseRedirect(reverse("course_list"))

            registration_form = forms.CourseRegistrationForm(
                course=course, user_profile=request.user.profile
            )
        else:
            registration_form = forms.CourseRegistrationForm(
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
            registration_form = forms.CourseRegistrationForm(
                data=request.POST, course=course, user_profile=request.user.profile
            )
        else:
            registration_form = forms.CourseRegistrationForm(
                data=request.POST, course=course
            )

        if registration_form.is_valid():
            if not request.user.is_authenticated:
                email = registration_form.cleaned_data.get("email")
                if CourseRegistration.objects.filter(email=email, course=course).exists():
                    registration_form.add_error("email", _(
                        "A registration with this email address already exists."))
                    return render(
                        request,
                        "register_course.html",
                        {
                            "course": course,
                            "form": registration_form,
                            "course_data": course_data,
                        },
                    )

            registration = registration_form.save(commit=False)
            registration.course = course

            selected_sessions = registration_form.cleaned_data.get(
                "selected_sessions")
            registration.final_fee = registration.calculate_fees(
                course, selected_sessions)
            registration.dinner = registration_form.cleaned_data.get("dinner")

            if request.user.is_authenticated:
                registration.user = request.user
                registration.set_exam(request.user)
            else:
                registration.set_exam()
                registration.email = registration_form.cleaned_data.get(
                    "email")
                registration.first_name = registration_form.cleaned_data.get(
                    "first_name")
                registration.last_name = registration_form.cleaned_data.get(
                    "last_name")

            registration.save()

            registration.selected_sessions.set(selected_sessions)

            try:
                utils.send_registration_confirmation(request, registration)
                utils.send_registration_notification(request, registration)
            except SMTPException as e:
                registration_form.add_error("email", e)
                registration.delete()
                return render(
                    request,
                    "register_course.html",
                    {
                        "course": course,
                        "form": registration_form,
                        "course_data": course_data,
                    },
                )

            messages.info(
                request,
                _("You have successfully signed up for ") + course.title
            )
            if request.user.is_authenticated:
                return HttpResponseRedirect(reverse("courseregistration_list"))
            return HttpResponseRedirect(reverse("course_list"))

        else:
            return render(
                request,
                "register_course.html",
                {
                    "course": course,
                    "form": registration_form,
                    "course_data": course_data,
                },
            )


class CourseRegistrationList(LoginRequiredMixin, View):
    """Displays a list of a users course registrations"""

    def get(self, request):
        user_registrations = CourseRegistration.objects.filter(
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
                "bank_account": os.environ.get("BANK_ACCOUNT"),
            },
        )


class CancelCourseRegistration(LoginRequiredMixin, SuccessMessageMixin, View):
    """Deletes a course registration instance"""

    def get(self, request, pk):
        registration = get_object_or_404(CourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied
        messages.warning(
            request,
            _("Please cancel registrations by clicking the button from the 'My Registrations' page.")
        )

        return HttpResponseRedirect(reverse("courseregistration_list"))

    def post(self, request, pk):
        registration = get_object_or_404(CourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        registration.delete()

        messages.success(
            request,
            _("Your registration for ") +
            registration.course.title + _("has been cancelled.")
        )
        return HttpResponseRedirect(reverse("courseregistration_list"))


class UpdateCourseRegistration(LoginRequiredMixin, View):
    """Updates a course registration"""

    def prepare_course_data(self, course):
        """Prepares data to be passed to the template"""
        course_data = {"course_fee": course.course_fee,
                       "course_fee_cash": course.course_fee_cash,
                       "course_fee_with_dan_preparation": course.course_fee_with_dan_preparation,
                       "course_fee_with_dan_preparation_cash": course.course_fee_with_dan_preparation_cash,
                       "discount_percentage": course.discount_percentage
                       }
        counter = 0
        for session in course.sessions.all():
            course_data[f"session_{counter}_fee"] = session.session_fee
            course_data[f"session_{counter}_fee_cash"] = session.session_fee_cash
            counter += 1
        return course_data

    def get(self, request, pk):
        registration = get_object_or_404(CourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        course = registration.course

        selected_sessions = registration.selected_sessions.all()

        registration_form = forms.CourseRegistrationForm(
            instance=registration,
            course=course,
            user_profile=request.user.profile,
            initial={"selected_sessions": selected_sessions},
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
        registration = get_object_or_404(CourseRegistration, pk=pk)

        if registration.user != request.user:
            raise PermissionDenied

        course = registration.course
        course_data = self.prepare_course_data(course)

        registration_form = forms.CourseRegistrationForm(
            data=request.POST,
            instance=registration,
            course=course,
            user_profile=request.user.profile,
        )

        if registration_form.is_valid():
            registration = registration_form.save(commit=False)
            selected_sessions = registration_form.cleaned_data.get(
                "selected_sessions")

            registration.final_fee = registration.calculate_fees(
                course, selected_sessions)
            registration.set_exam(request.user)
            registration.save()

            registration.selected_sessions.set(selected_sessions)

            messages.info(
                request,
                _("You have successfully updated your registration for ") +
                f"{course.title}",
            )

            return HttpResponseRedirect(reverse("courseregistration_list"))

        else:
            if not registration_form.cleaned_data.get("selected_sessions"):
                messages.warning(
                    request,
                    _("Registration not submitted. Please select at least one session.")
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


class ExportCourseRegistrations(LoginRequiredMixin, UserPassesTestMixin, View):
    """Exports course registrations as a CSV file"""

    def test_func(self):
        return self.request.user.is_staff and self.request.user.groups.filter(name='Course Team').exists()

    def get(self, request, slug):
        queryset = CourseRegistration.objects.filter(course__slug=slug)
        if not queryset.exists():
            messages.warning(request, _(
                "No registrations found for this course."))
            return HttpResponseRedirect(reverse("home"))

        messages.success(request, _("Download started"))

        return render(request, 'export_redirect.html', {'slug': slug})

    def post(self, request, slug):
        if request.method == "POST":
            queryset = CourseRegistration.objects.filter(course__slug=slug)
            if not queryset.exists():
                messages.warning(request, _(
                    "No registrations found for this course."))
                return HttpResponseRedirect(reverse("home"))

            filename = f"csv_export_{slugify(slug)}_{date.today()}.csv"
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename={filename}'

            writer = csv.writer(response)
            utils.write_registrations_csv(writer, queryset)

            return response
        else:
            messages.error(request, _("Invalid request method."))
            return HttpResponseRedirect(reverse("home"))
