from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class FeesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "fees"
    verbose_name = _("Fees")
