from django.http import Http404


def catch_all_404_view(request):
    raise Http404("Page not found")
