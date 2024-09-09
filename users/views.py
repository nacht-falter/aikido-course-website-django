from datetime import date

from allauth.account.views import PasswordChangeView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View

from course_registrations.models import CourseRegistration
from danbw_website import constants, utils

from . import forms
from .models import User, UserProfile


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
        profile_form = forms.UserProfileForm()
        return render(
            request,
            "create_userprofile.html",
            {"form": profile_form},
        )

    def post(self, request):
        profile_form = forms.UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            user_profile = UserProfile.objects.create(
                user=request.user,
                grade=profile_form.cleaned_data["grade"],
                dojo=profile_form.cleaned_data["dojo"]
            )
            user_profile.user.first_name = profile_form.cleaned_data[
                "first_name"
            ]
            user_profile.user.last_name = profile_form.cleaned_data[
                "last_name"
            ]
            user_profile.user.save()
            user_profile.save()
            messages.info(
                request,
                _("You have successfully created a user profile.")
            )

            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse("userprofile"))

        else:
            return render(
                request,
                "create_userprofile.html",
                {"form": profile_form}
            )


class UpdateUserProfile(LoginRequiredMixin, View):
    """Displays a form to update user information"""

    def get(self, request):
        user_profile = get_object_or_404(UserProfile, user=request.user)

        dojos = {choice[0] for choice in constants.DOJO_CHOICES}
        dojo_key = utils.get_tuple_key(
            constants.DOJO_CHOICES, user_profile.dojo)

        if dojo_key in dojos:
            dojo_initial = dojo_key
            other_dojo_initial = ""
        else:
            dojo_initial = "other"
            other_dojo_initial = user_profile.dojo

        profile_form = forms.UpdateUserProfileForm(
            initial={
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "grade": user_profile.grade,
                "dojo": dojo_initial,
                "other_dojo": other_dojo_initial,
            }
        )

        return render(
            request,
            "update_userprofile.html",
            {"form": profile_form},
        )

    def post(self, request):
        queryset = UserProfile.objects.filter(user=request.user)
        user_profile = get_object_or_404(queryset, user=request.user)
        profile_form = forms.UpdateUserProfileForm(data=request.POST)
        if profile_form.is_valid():
            user_profile.user.first_name = profile_form.cleaned_data[
                "first_name"
            ]
            user_profile.user.last_name = profile_form.cleaned_data[
                "last_name"
            ]
            user_profile.grade = profile_form.cleaned_data["grade"]
            user_profile.dojo = profile_form.cleaned_data["dojo"]
            user_profile.user.save()
            user_profile.save()
            messages.info(
                request,
                _("You have successfully updated your user profile.")
            )

            next_url = request.GET.get('next')
            if next_url:
                return HttpResponseRedirect(next_url)
            return HttpResponseRedirect(reverse("userprofile"))

        else:
            return render(
                request,
                "update_userprofile.html",
                {"form": profile_form},
            )


class UpdateGrade(View):
    """Updates a user's grade"""

    def get(self, request):
        exam_registration = CourseRegistration.objects.filter(
            user=request.user, grade_updated=False
        ).first()
        if (
            exam_registration
            and exam_registration.course.end_date <= date.today()
        ):
            return render(
                request,
                "update_grade.html",
                {"exam_registration": exam_registration},
            )
        return HttpResponseRedirect(reverse("home"))

    def post(self, request):
        answer = request.POST.get("answer")
        exam_registration = CourseRegistration.objects.filter(
            user=request.user, grade_updated=False
        ).first()
        if answer == "yes":
            user_profile = get_object_or_404(UserProfile, user=request.user)
            user_profile.grade = exam_registration.exam_grade
            user_profile.save()
            exam_registration.grade_updated = True
            exam_registration.exam_passed = True
            exam_registration.save()
            messages.info(
                request,
                _("Congratulations! Your grade has been updated to ") +
                f"{user_profile.get_grade_display()}.",
            )
        else:
            exam_registration.grade_updated = True
            exam_registration.save()
            messages.info(request, _("Your grade has not been updated."))

        return HttpResponseRedirect(reverse("home"))


class DeactivateUser(LoginRequiredMixin, View):
    """Deactivates a user accounts
    The Django docs recommend to deactivate user accounts instead
    of deleting them to avoid breaking foreign keys:
    https://docs.djangoproject.com/en/4.2/ref/contrib/auth/#django
    .contrib.auth.models.User.is_active
    """

    def get(self, request):
        messages.warning(
            request,
            _("Please use the button on the user profile page for deactivating your account."),
        )
        return HttpResponseRedirect(reverse("userprofile"))

    def post(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                request.user.is_active = False
                request.user.save()
                messages.info(
                    request, _(
                        "You have successfully deactivated your account.")
                )
                return redirect(reverse("course_list"))
            else:
                messages.warning(
                    request,
                    _("Staff accounts cannot be deactivated. Please contact us if you want to deactivate your account."),
                )
                return redirect(reverse("userprofile"))
        else:
            messages.error(
                request, _("You must be logged in to deactivate your account.")
            )
            return redirect(reverse("userprofile"))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Overrides the redirect URL for the allauth PasswordChangeView
    Instructions from: https://stackoverflow.com/a/56599071
    """

    success_url = reverse_lazy("userprofile")
