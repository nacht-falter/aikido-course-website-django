from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from courses.models import InternalCourse
from danbw_website import constants


class Fee(models.Model):
    FEE_TYPES = [
        ("regular", _("Regular")),
        ("dan_seminar", _("Dan Seminar")),
    ]

    FEE_CATEGORIES = [
        ("single_session", _("Single Session")),
        ("entire_course", _("Entire Course")),
        ("dan_prep", _("Dan Preparation Session")),
        ("entire_course_dan_prep", _("Entire Course with Dan Preparation")),
        ("single_day", _("Single Day")),
    ]

    course_type = models.CharField(
        _("Course Type"),
        max_length=50,
        choices=InternalCourse.COURSE_TYPES,
    )
    fee_type = models.CharField(
        _("Fee Type"),
        max_length=50,
        choices=FEE_TYPES,
    )
    fee_category = models.CharField(
        _("Fee Category"),
        max_length=50,
        choices=FEE_CATEGORIES,
        null=True,
        blank=True,
    )
    dan_discount = models.BooleanField(
        _("D.A.N. Discount"),
        default=False
    )
    payment_method = models.IntegerField(
        _("Payment method"),
        choices=constants.PAYMENT_METHODS,
        default=0,
    )
    amount = models.DecimalField(_("Amount"), max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = _("Fee")
        verbose_name_plural = _("Fees")
        unique_together = ['course_type', 'fee_type',
                           'fee_category', 'dan_discount', 'payment_method']

    def __str__(self):
        fee_type_display = (
            f"{self.get_fee_type_display()} - {self.get_fee_category_display()}"
            if self.fee_category else self.get_fee_type_display()
        )
        discount_status = _(
            "D.A.N. Discount") if self.dan_discount else _("No Discount")
        return f"{self.course_type} - {fee_type_display} ({discount_status}) - {self.get_payment_method_display()}"

    @classmethod
    def get_fee(cls, course_type, fee_type='regular', fee_category=None, payment_method='bank', dan_discount=False):
        try:
            fee = cls.objects.get(
                course_type=course_type,
                fee_type=fee_type,
                fee_category=fee_category,
                payment_method=payment_method,
                dan_discount=dan_discount
            )
            return fee.amount
        except cls.DoesNotExist:
            return None

    def clean(self):
        if self.fee_type == "dan_seminar" and self.fee_category not in ["single_day", "entire_course"]:
            raise ValidationError(_("Invalid fee category for Dan Seminar."))
        super().clean()
