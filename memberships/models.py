from django.core.validators import RegexValidator
from django.db import models

from danbw_website import constants


class DanIntMembership(models.Model):
    """Represents a DAN International Membership"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    street = models.CharField(max_length=100)
    street_number = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10, validators=[RegexValidator(
        regex='^[0-9]{1,10}$', message='Enter a valid postcode.', code='invalid_postcode')])
    email = models.EmailField(unique=True)
    phone_home = models.CharField(max_length=100, validators=[RegexValidator(
        regex='^\+?1?\d{9,15}$', message='Enter a valid phone number.', code='invalid_phone_number')], blank=True)
    phone_mobile = models.CharField(max_length=100, validators=[RegexValidator(
        regex='^\+?1?\d{9,15}$', message='Enter a valid phone number.', code='invalid_phone_number')], blank=True)
    grade = models.IntegerField(choices=constants.GRADE_CHOICES)
    dojo = models.CharField(choices=constants.DOJO_CHOICES, max_length=100)
    other_dojo = models.CharField(max_length=100, blank=True)
    sepa = models.BooleanField("SEPA", default=False)
    account_holder = models.CharField(max_length=100)
    iban = models.CharField("IBAN", max_length=34)
    accept_terms = models.BooleanField(default=False, blank=False)
    liability_disclaimer = models.BooleanField(default=False, blank=False)
    comment = models.TextField(blank=True)

    class Meta:
        verbose_name = "DAN International Membership"
        verbose_name_plural = "DAN International Memberships"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
