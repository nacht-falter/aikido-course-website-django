from django.contrib import messages
from django.urls import reverse_lazy
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
            email = form.cleaned_data["email"]

            utils.send_membership_confirmation(first_name, email)

            message = "We have received your membership application. Please check your email for a confirmation."
            messages.success(self.request, message)

            return super().form_valid(form)
