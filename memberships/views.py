import os
from smtplib import SMTPException

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from danbw_website import constants, utils

from .forms import (ChildrensPassportForm, DanBwMembershipForm,
                    DanIntMembershipForm)
from .models import ChildrensPassport, DanBwMembership, DanIntMembership


class BaseMembershipCreateView(generic.CreateView):
    success_url = reverse_lazy("home")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["fees"] = dict(constants.MEMBERSHIP_FEES)
        context["bank_details"] = os.environ.get("BANK_ACCOUNT")
        context["membership_type"] = self.membership_type
        return context

    def form_valid(self, form):
        first_name = form.cleaned_data["first_name"]
        last_name = form.cleaned_data["last_name"]
        email = form.cleaned_data["email"]
        dojo = utils.get_tuple_value(
            constants.DOJO_CHOICES, form.cleaned_data["dojo"])

        try:
            utils.send_membership_confirmation(
                first_name, email, self.membership_type)
            utils.send_membership_notification(
                first_name, last_name, email, dojo, self.membership_type)
        except SMTPException as e:
            messages.error(self.request, e)
            return self.form_invalid(form)

        message = (
            _("We have received your membership application.") +
            _(" Please check your email for confirmation.")
        )
        messages.success(self.request, message)

        return super().form_valid(form)


class DanIntMembershipCreateView(BaseMembershipCreateView):
    template_name = "membership_form.html"
    model = DanIntMembership
    form_class = DanIntMembershipForm
    membership_type = "dan_international"

    from .forms import ChildrensPassportForm


class ChildrensPassportCreateView(BaseMembershipCreateView):
    template_name = "childrens_passport_form.html"
    model = ChildrensPassport
    form_class = ChildrensPassportForm
    membership_type = "childrens_passport"


class DanBwMembershipCreateView(BaseMembershipCreateView):
    model = DanBwMembership
    template_name = "membership_form.html"
    form_class = DanBwMembershipForm
    membership_type = "danbw"
