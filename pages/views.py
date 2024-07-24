from datetime import date

from django.conf import settings
from django.contrib import messages
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.utils.translation import gettext as _
from django.views import View, generic

from course_registrations.models import CourseRegistration
from courses.models import ExternalCourse, InternalCourse

from . import forms
from .models import Category, Page


class HomePage(View):
    """Displays the home page"""

    def get(self, request):
        all_courses = list(InternalCourse.objects.all()) + \
            list(ExternalCourse.objects.all())

        for course in all_courses:
            if request.user.is_authenticated and course.get_course_type == "InternalCourse":
                course.user_registered = CourseRegistration.objects.filter(
                    user=request.user, course=course
                )
            course.save()

        upcoming_courses = [
            course for course in all_courses if course.end_date >= date.today()
        ]
        upcoming_registrations = []
        if request.user.is_authenticated:
            all_registrations = CourseRegistration.objects.filter(
                user=request.user
            )
            upcoming_registrations = [
                registration
                for registration in all_registrations
                if registration.course.end_date >= date.today()
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
                    request, _("Invalid Header found. Please try again.")
                )
                return HttpResponseRedirect(reverse("contact"))
            messages.success(request, _(
                "Thank you! Your message has been sent."))
        else:
            contact_form = forms.ContactForm()
            return render(
                request,
                "contact.html",
                {"form": contact_form},
            )

        return HttpResponseRedirect(reverse("home"))


class PageDetail(generic.DetailView):
    """Displays a single page"""
    model = Page
    template_name = "page_detail.html"
    context_object_name = "page"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    queryset = Page.objects.filter(status=1)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.get_object()
        similar_pages = Page.objects.filter(
            category=page.category, status=1).exclude(id=page.id)
        context['category_slug'] = page.category.slug
        context['page_slug'] = page.slug
        context['similar_pages'] = similar_pages
        return context
