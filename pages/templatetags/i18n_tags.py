from django import template
from django.urls import resolve, reverse
from django.utils import translation
from danbw_website import constants

register = template.Library()

@register.filter
def get_flag(lang_code):
    """
    Takes a language code and returns the corresponding Unicode flag emoji.
    """
    return constants.LANGUAGE_FLAGS.get(lang_code, "")


@register.simple_tag(takes_context=True)
def change_lang(context, lang_code, *args, **kwargs):
    """
    Gets the URL for the current page in the selected language.
    It resolves the current URL's view name and arguments and then
    reverses it in the target language.
    """
    request = context.get('request')
    if not request:
        # Fallback if no request in context (e.g., during tests)
        return f"/{lang_code}/"

    path = request.path
    try:
        url_parts = resolve(path)

        with translation.override(lang_code):
            # Reverse the URL with the original view name, args, and kwargs
            new_url = reverse(url_parts.view_name, args=url_parts.args, kwargs=url_parts.kwargs)

        return new_url
    except Exception:
        # Fallback to the homepage for the target language if reversing fails
        return f"/{lang_code}/"
