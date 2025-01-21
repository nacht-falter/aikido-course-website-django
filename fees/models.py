from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from danbw_website import constants


class Fee(models.Model):
    FEE_TYPES = [
        ("single_session", _("Single Session")),
        ("entire_course", _("Entire Course")),
        ("single_day", _("Single Day")),
        ("single_session_dan_preparation", _("Dan Preparation Session")),
        ("entire_course_dan_preparation", _("Entire Course with Dan Preparation")),
    ]

    course_type = models.CharField(
        _("Course Type"),
        max_length=50,
        choices=constants.COURSE_TYPES,
    )
    fee_category = models.CharField(
        _("Fee Category"),
        max_length=50,
        choices=constants.FEE_CATEGORIES,
        null=True,
        blank=True,
    )
    fee_type = models.CharField(
        _("Fee Type"),
        max_length=50,
        choices=FEE_TYPES,
    )
    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    extra_fee_external = models.DecimalField(
        _("Extra Fee External"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    extra_fee_cash = models.DecimalField(
        _("Extra Fee Cash"),
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = _("Fee")
        verbose_name_plural = _("Fees")
        unique_together = ['course_type', 'fee_category', 'fee_type']

    @classmethod
    def get_fee(
        cls,
        course_type,
        fee_category,
        fee_type,
        payment_method,
        dan_member,
        default=0
    ):
        """
        Calculate the total fee based on the provided parameters.
        """
        try:
            fee = cls.objects.get(
                course_type=course_type,
                fee_category=fee_category,
                fee_type=fee_type,
            )
            return (
                fee.amount
                + (fee.extra_fee_cash if payment_method == 1 else 0)
                + (fee.extra_fee_external if not dan_member else 0)
            )
        except cls.DoesNotExist:
            return default
