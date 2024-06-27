from smtplib import SMTPException

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from danbw_website import utils
from danbw_website.constants import DOJO_CHOICES

from .forms import DanIntMembershipForm, ChildrensPassportForm
from .models import DanIntMembership, ChildrensPassport


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
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]
        dojo = utils.get_tuple_value(
            DOJO_CHOICES, form.cleaned_data["dojo"])

        try:
            utils.send_membership_confirmation(
                first_name, email, "dan_international")
            utils.send_membership_notification(
                first_name, last_name, email, dojo, "dan_international")
        except SMTPException as e:
            messages.error(self.request, e)
            return self.form_invalid(form)

        message = (
            _("We have received your membership application.") +
            _(" Please check your email for confirmation.")
        )
        messages.success(self.request, message)

        return super().form_valid(form)


class ChildrensPassportCreateView(generic.CreateView):
    model = ChildrensPassport
    template_name = "childrens_passport_form.html"
    success_url = reverse_lazy("home")
    form_class = ChildrensPassportForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]
        dojo = utils.get_tuple_value(
            DOJO_CHOICES, form.cleaned_data["dojo"])

        try:
            utils.send_membership_confirmation(
                first_name, email, _("childrens_passport"))
            utils.send_membership_notification(
                first_name, last_name, email, dojo, "childrens_passport")
        except SMTPException as e:
            messages.error(self.request, e)
            return self.form_invalid(form)

        message = (
            _("We have received your application.") +
            _(" Please check your email for confirmation.")
        )
        messages.success(self.request, message)

        return super().form_valid(form)
