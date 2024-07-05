from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from danbw_website import constants

from .models import ChildrensPassport, DanBwMembership, DanIntMembership


class BaseMembershipForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    first_name = forms.CharField(label=_("First Name"), max_length=100)
    last_name = forms.CharField(label=_("Last Name"), max_length=100)
    date_of_birth = forms.DateField(label=_("Date of Birth"))
    street = forms.CharField(label=_("Street"), max_length=100)
    street_number = forms.CharField(label=_("Street Number"), max_length=10)
    city = forms.CharField(label=_("City"), max_length=100)
    postcode = forms.CharField(
        label=_("Postcode"),
        max_length=10,
        validators=[RegexValidator(
            regex=r"^[0-9]{1,10}$",
            message=_("Enter a valid postcode."),
            code="invalid_postcode"
        )],
    )
    email = forms.EmailField(label=_("Email"), max_length=100)
    phone_home = forms.CharField(
        label=_("Home Phone"),
        max_length=100,
        validators=[RegexValidator(
            regex=r"^\+?1?\d{9,15}$",
            message=_("Enter a valid phone number."),
            code="invalid_phone_number"
        )],
        required=False,
    )
    phone_mobile = forms.CharField(
        label=_("Mobile Phone"),
        max_length=100,
        validators=[RegexValidator(
            regex=r"^\+?1?\d{9,15}$",
            message=_("Enter a valid phone number."),
            code="invalid_phone_number"
        )],
        required=False,
    )
    grade = forms.ChoiceField(
        label=_("Grade"), choices=constants.GRADE_CHOICES)
    dojo = forms.ChoiceField(label=_("Dojo"), choices=constants.DOJO_CHOICES)
    other_dojo = forms.CharField(
        label=_("Other Dojo"), max_length=100, required=False)
    liability_disclaimer = forms.BooleanField(
        required=True,
        label=_(
            "I am aware that Aikido is a potentially dangerous sport and that the above-mentioned organization "
            "and its representatives are not liable for accidents or injuries that occur during the practice of "
            "Aikido, except within the scope of legal regulations in cases of intent or gross negligence."
        ),
    )
    comment = forms.CharField(
        label=_("Comment"), widget=forms.Textarea, required=False)
    passport_issued = forms.BooleanField(
        label=_("Passport Issued"), required=False)

    class Meta:
        abstract = True


class DanIntMembershipForm(BaseMembershipForm):
    sepa = forms.BooleanField(
        required=True,
        label=_(
            "I agree that the membership fee will be collected by SEPA direct debit from my account below."),
    )
    accept_terms = forms.BooleanField(
        required=True,
        label=_(
            "I have read and accept the statutes of DAN International and agree to the terms and conditions "
            "regarding cancellation and data processing. I hereby apply for membership with DAN International."
        ),
    )
    account_holder = forms.CharField(label=_("Account Holder"), max_length=100)
    iban = forms.CharField(label=_("IBAN"), max_length=34)

    class Meta:
        model = DanIntMembership
        fields = '__all__'


class ChildrensPassportForm(BaseMembershipForm):
    name_legal_guardian = forms.CharField(
        label=_("Name of Legal Guardian"), max_length=100)
    accept_terms = forms.BooleanField(
        required=True,
        label=_("I accept the above terms and conditions and apply for a children's passport."),
    )

    class Meta:
        model = ChildrensPassport
        fields = '__all__'

        from django import forms


class DanBwMembershipForm(BaseMembershipForm):
    accept_terms = forms.BooleanField(
        required=True,
        label=_(
            "I have read the statutes of DANBW e.V. and agree to the terms and conditions above. "
            "I hereby apply for a membership with DANBW."
        ),
    )
    class Meta:
        model = DanBwMembership
        fields = '__all__'
