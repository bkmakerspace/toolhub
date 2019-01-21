from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.shortcuts import get_current_site
from django_jinja import library
import jinja2


@library.global_function
@jinja2.contextfunction
def get_flatpages(context, starts_with=None, user=None):
    if "request" in context:
        site_pk = get_current_site(context["request"]).pk
    else:
        site_pk = settings.SITE_ID
    flatpages = FlatPage.objects.filter(sites__id=site_pk)
    # If a prefix was specified, add a filter
    if starts_with:
        flatpages = flatpages.filter(url__startswith=starts_with)

    # If the provided user is not authenticated, or no user
    # was provided, filter the list to only public flatpages.
    if not user or not user.is_authenticated:
        flatpages = flatpages.filter(registration_required=False)

    return flatpages
