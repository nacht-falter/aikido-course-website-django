from smtplib import SMTPException

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from danbw_website import utils

from .forms import DanIntMembershipForm
from .models import DanIntMembership


class DanIntMembershipCreateView(generic.CreateView):
    model = DanIntMembership
    template_name = "membership_form.html"
    success_url = reverse_lazy("home")
    form_class = DanIntMembershipForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        if form.is_valid():

            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]

            try:
                utils.send_membership_confirmation(
                    first_name, email, "DAN International")
                utils.send_membership_notification(
                    first_name, last_name, email, "DAN International")
            except SMTPException as e:
                messages.error(self.request, e)
                return self.form_invalid(form)

            message = (
                _("We have received your membership application.") +
                _(" Please check your email for confirmation.")
            )
            messages.success(self.request, message)

            return super().form_valid(form)
