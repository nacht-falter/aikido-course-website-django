from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from danbw_website import constants


class BaseMembership(models.Model):
    """Base model for common memberships"""
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    date_of_birth = models.DateField(_("Date of Birth"))
    street = models.CharField(_("Street"), max_length=100)
    street_number = models.CharField(_("Street Number"), max_length=10)
    city = models.CharField(_("City"), max_length=100)
    postcode = models.CharField(
        _("Postcode"),
        max_length=10,
        validators=[RegexValidator(
            regex=r"^[0-9]{1,10}$",
            message=_("Enter a valid postcode."),
            code="invalid_postcode"
        )],
    )
    email = models.EmailField(unique=True, verbose_name=_("Email"))
    phone_home = models.CharField(
        _("Home Phone"),
        max_length=100,
        validators=[RegexValidator(
            regex=r"^\+?1?\d{9,15}$",
            message=_("Enter a valid phone number."),
            code="invalid_phone_number"
        )],
        blank=True,
    )
    phone_mobile = models.CharField(
        _("Mobile Phone"),
        max_length=100,
        validators=[RegexValidator(
            regex=r"^\+?1?\d{9,15}$",
            message=_("Enter a valid phone number."),
            code="invalid_phone_number"
        )],
        blank=True,
    )
    grade = models.IntegerField(_("Grade"), choices=constants.GRADE_CHOICES)
    dojo = models.CharField(
        _("Dojo"),
        choices=constants.DOJO_CHOICES,
        max_length=100
    )
    other_dojo = models.CharField(_("Other Dojo"), max_length=100, blank=True)
    accept_terms = models.BooleanField(
        _("Accept Terms"),
        default=False,
        blank=False
    )
    liability_disclaimer = models.BooleanField(
        _("Liability Disclaimer"),
        default=False,
        blank=False
    )
    comment = models.TextField(_("Comment"), blank=True)
    passport_issued = models.BooleanField(_("Passport Issued"), default=False)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class DanIntMembership(BaseMembership):
    """Represents a DAN International Membership"""
    sepa = models.BooleanField(_("SEPA Mandate"), default=False)
    account_holder = models.CharField(_("Account Holder"), max_length=100)
    iban = models.CharField(_("IBAN"), max_length=34)

    class Meta:
        verbose_name = _("DAN International Membership")
        verbose_name_plural = _("DAN International Memberships")


class ChildrensPassport(BaseMembership):
    """Represents a Childrens Passport"""
    name_legal_guardian = models.CharField(
        _("Name of Legal Guardian"),
        max_length=100
    )

    class Meta:
        verbose_name = _("Childrens Passport")
        verbose_name_plural = _("Childrens Passports")


class DanBwMembership(BaseMembership):
    """Represents a DANBW Membership"""

    class Meta:
        verbose_name = _("DANBW Membership")
        verbose_name_plural = _("DANBW Memberships")
