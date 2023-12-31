from datetime import date

from django.shortcuts import render, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.core.exceptions import PermissionDenied

from allauth.account.views import PasswordChangeView

from .models import Course, CourseRegistration, UserProfile, Page, Category
from . import forms

CURRENT_DATE = date.today()


class HomePage(View):
    """Displays the home page"""

    def get(self, request):
        all_courses = Course.objects.all()
        upcoming_courses = [
            course for course in all_courses if course.end_date >= CURRENT_DATE
        ]
        upcoming_registrations = []
        if request.user.is_authenticated:
            all_registrations = CourseRegistration.objects.filter(
                user=request.user
            )
            upcoming_registrations = [
                registration
                for registration in all_registrations
                if registration.course.end_date >= CURRENT_DATE
            ]

        return render(
            request,
            "index.html",
            {
                "upcoming_courses": upcoming_courses,
                "upcoming_registrations": upcoming_registrations,
            },
        )


class ContactPage(View):
    """Displays contact information and a contact form
    Instructions from: https://learndjango.com/tutorials/django-email-
    contact-form-tutorial
    """

    def get(self, request):
        contact_form = forms.ContactForm()
        return render(
            request,
            "contact.html",
            {"form": contact_form},
        )

    def post(self, request):
        contact_form = forms.ContactForm(data=request.POST)
        if contact_form.is_valid():
            subject = contact_form.cleaned_data["subject"]
            from_email = contact_form.cleaned_data["from_email"]
            message = contact_form.cleaned_data["message"]
            try:
                send_mail(
                    subject,
                    message,
                    from_email,
                    [settings.EMAIL_HOST_USER],
                )
            except BadHeaderError:
                messages.warning(
                    request, "Invalid Header found. Please try again."
                )
                return HttpResponseRedirect(reverse("contact"))
            messages.success(request, "Thank you! Your message has been sent.")
        else:
            contact_form = forms.ContactForm()
            return render(
                request,
                "contact.html",
                {"form": contact_form},
            )

        return HttpResponseRedirect(reverse("home"))


class PageList(generic.ListView):
    """Displays a list of pages from a category"""

    model = Page
    template_name = "page_list.html"

    def get_queryset(self):
        category_slug = self.kwargs.get("category_slug")
        category = get_object_or_404(Category, slug=category_slug)
        return Page.objects.filter(status=1, category=category)


class CourseList(generic.ListView):
    """Displays a list of all courses"""

    model = Course
    queryset = Course.objects.all()
    template_name = "course_list.html"


class RegisterCourse(LoginRequiredMixin, View):
    """Creates a course registration"""

    def prepare_course_data(self, course):
        """Prepares data to be passed to the template"""
        course_data = {"course_fee": course.course_fee}
        counter = 0
        for session in course.sessions.all():
            course_data[f"session_{counter}_fee"] = session.session_fee
            counter += 1
        return course_data

    def get(self, request, slug):
        user_profile = UserProfile.objects.filter(user=request.user)
        if not user_profile:
            messages.warning(
                request, "Please create a user profile and try again."
            )
            return HttpResponseRedirect(reverse("userprofile"))

        courses = Course.objects.filter(registration_status=1)
        course = get_object_or_404(courses, slug=slug)

        course_data = self.prepare_course_data(course)

        user_registered = CourseRegistration.objects.filter(
            user=request.user, course=course
        )

        if user_registered:
            messages.warning(
                request, "You are already registered for this course."
            )
            return HttpResponseRedirect(reverse("course_list"))

        registration_form = forms.CourseRegistrationForm(
            course=course, user_profile=request.user.profile
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
        queryset = Course.objects.filter(registration_status=1)
        course = get_object_or_404(queryset, slug=slug)
        course_data = self.prepare_course_data(course)

        registration_form = forms.CourseRegistrationForm(
            data=request.POST, course=course, user_profile=request.user.profile
        )
        if registration_form.is_valid():
            registration = registration_form.save(commit=False)
            registration.course = course
            registration.user = request.user

            selected_sessions = registration_form.cleaned_data.get(
                "selected_sessions"
            )

            registration.final_fee = registration.calculate_fees(
                course, selected_sessions
            )

            registration.set_exam(request.user)

            registration.save()

            # Update the registration to include the selected sessions.
            # Instructions on how to save objects with a many-
            # to-many field: https://docs.djangoproject.com/en/4.2/ref
            # /models/relations/#django.db.models.fields.related.Relat
            # edManager.set
            registration.selected_sessions.set(selected_sessions)

            # Send confirmation email:
            exam = (
                registration.get_exam_grade_display()
                if registration.exam
                else "None"
            )
            sessions = [session.title for session in selected_sessions]
            send_mail(
                # Subject:
                f"[DANBW e.V.] You signed up for {registration.course}",
                # Message content:
                f"Hi {registration.user},\n"
                "You have succesfully signed up "
                f"for {course}\n"
                f"\nCourse dates: {course.start_date.strftime('%b %d')} "
                f"to {course.end_date.strftime('%b %d, %Y')}\n"
                "\nRegistration details:\n"
                f"- Selected sessions: "
                f"{(', '.join(sessions))}\n"
                f"- Exam: {exam}\n"
                f"- Fee: {registration.final_fee} €",
                # Sender:
                settings.EMAIL_HOST_USER,
                # Recipient:
                [registration.user.email],
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

            registration_form = forms.CourseRegistrationForm(
                course=course, user_profile=request.user.profile
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

        return HttpResponseRedirect(reverse("courseregistration_list"))


class CourseRegistrationList(LoginRequiredMixin, View):
    """Displays a list of a users course registrations"""

    def get(self, request):
        user_registrations = CourseRegistration.objects.filter(
            user=request.user
        )
        past_registrations = [
            registration
            for registration in user_registrations
            if registration.course.end_date < CURRENT_DATE
        ]
        upcoming_registrations = [
            registration
            for registration in user_registrations
            if registration.course.end_date >= CURRENT_DATE
        ]

        return render(
            request,
            "courseregistration_list.html",
            {
                "past_registrations": past_registrations,
                "upcoming_registrations": upcoming_registrations,
            },
        )


class CancelCourseRegistration(LoginRequiredMixin, SuccessMessageMixin, View):
    """Deletes a course registration instance"""

    def get(self, request, pk):
        registration = get_object_or_404(CourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied
        else:
            messages.warning(
                request,
                "Please cancel registrations by clicking the button from the "
                "My Registrations page.",
            )

        return HttpResponseRedirect(reverse("courseregistration_list"))

    def post(self, request, pk):
        registration = get_object_or_404(CourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        registration.delete()

        messages.success(
            request,
            f"Your registration for {registration.course.title} "
            "has been cancelled.",
        )
        return HttpResponseRedirect(reverse("courseregistration_list"))


class UpdateCourseRegistration(LoginRequiredMixin, View):
    """Updates a course registration"""

    def prepare_course_data(self, course):
        """Prepares data to be passed to the template"""
        course_data = {"course_fee": course.course_fee}
        counter = 0
        for session in course.sessions.all():
            course_data[f"session_{counter}_fee"] = session.session_fee
            counter += 1
        return course_data

    def get(self, request, pk):
        registration = get_object_or_404(CourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        course = registration.course
        registration_form = forms.CourseRegistrationForm(
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
        registration = get_object_or_404(CourseRegistration, pk=pk)
        if registration.user != request.user:
            raise PermissionDenied

        course = registration.course
        registration_form = forms.CourseRegistrationForm(
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
            registration_form = forms.CourseRegistrationForm(
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
                request, "You have successfully created a user profile."
            )
        else:
            profile_form = forms.UserProfileForm()

        return HttpResponseRedirect(reverse("userprofile"))


class UpdateUserProfile(LoginRequiredMixin, View):
    """Displays a form to update user information"""

    def get(self, request):
        queryset = UserProfile.objects.filter(user=request.user)
        user_profile = get_object_or_404(queryset, user=request.user)

        profile_form = forms.UpdateUserProfileForm(
            initial={
                "username": request.user.username,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "email": request.user.email,
                "grade": user_profile.grade,
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
            user_profile.user.username = profile_form.cleaned_data["username"]
            user_profile.user.first_name = profile_form.cleaned_data[
                "first_name"
            ]
            user_profile.user.last_name = profile_form.cleaned_data[
                "last_name"
            ]
            user_profile.user.email = profile_form.cleaned_data["email"]
            user_profile.grade = profile_form.cleaned_data["grade"]
            user_profile.user.save()
            user_profile.save()
            messages.info(
                request, "You have successfully updated your user profile."
            )
        else:
            profile_form = forms.UpdateUserProfileForm()

        return HttpResponseRedirect(reverse("userprofile"))


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

        else:
            return HttpResponseRedirect(reverse("home"))

    def post(self, request):
        answer = request.POST.get("answer")
        exam_registration = CourseRegistration.objects.filter(
            user=request.user, grade_updated=False
        ).first()
        if answer == "yes":
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.grade = exam_registration.exam_grade
            user_profile.save()
            exam_registration.grade_updated = True
            exam_registration.exam_passed = True
            exam_registration.save()
            messages.info(
                request,
                "Congratulations! Your grade has been updated to"
                f" {user_profile.get_grade_display()}.",
            )
        else:
            exam_registration.grade_updated = True
            exam_registration.save()
            messages.info(request, "Your grade has not been updated.")

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
            "Please use the button on the user profile page for "
            "deactivating your account.",
        )
        return HttpResponseRedirect(reverse("userprofile"))

    def post(self, request):
        if not request.user.is_staff:
            user = User.objects.get(pk=request.user.pk)
            user.is_active = False
            user.save()
            messages.info(
                request, "You have successfully deactivated your account."
            )
            return HttpResponseRedirect(reverse("course_list"))
        else:
            messages.warning(
                request,
                "Staff accounts can not be deactivated."
                " Please contact us if you want to deactivate your account.",
            )
            return HttpResponseRedirect(reverse("userprofile"))


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    """Overrides the redirect URL for the allauth PasswordChangeView
    Instructions from: https://stackoverflow.com/a/56599071
    """

    success_url = reverse_lazy("userprofile")
