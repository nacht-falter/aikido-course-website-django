from django.apps import AppConfig


class CourseRegistrationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "course_registration"

    # Instructions for importing signals:
    # https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/
    def ready(self):
        import course_registration.signals
