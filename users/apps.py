from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = _("Users")

    # Instructions for importing signals:
    # https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/
    def ready(self):
        from . import signals
