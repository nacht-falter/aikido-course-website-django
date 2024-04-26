from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Instructions for importing signals:
    # https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/
    def ready(self):
        from . import signals
