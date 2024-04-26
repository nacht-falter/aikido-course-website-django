from .models import Category


def add_categories_to_context(request):
    """Context processor to pass categories to templates
    Adapted from: https://stackoverflow.com/a/34903331
    Django documentation for context processors:
    https://docs.djangoproject.com/en/4.2/ref/templates/api/#writing-
    your-own-context-processors
    """
    categories = Category.objects.all()
    return {"categories": categories}
