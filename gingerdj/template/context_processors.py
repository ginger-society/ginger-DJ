"""Provides the context processors in templates."""

import itertools

from gingerdj.conf import settings
from gingerdj.middleware.csrf import get_token
from gingerdj.utils.functional import SimpleLazyObject, lazy


def csrf(request):
    """
    Context processor that provides a CSRF token, or the string 'NOTPROVIDED' if
    it has not been provided by either a view decorator or the middleware
    """

    def _get_val():
        token = get_token(request)
        if token is None:
            # In order to be able to provide debugging info in the
            # case of misconfiguration, we use a sentinel value
            # instead of returning an empty dict.
            return "NOTPROVIDED"
        else:
            return token

    return {"csrf_token": SimpleLazyObject(_get_val)}


def debug(request):
    """
    Return context variables helpful for debugging.
    """
    context_extras = {}
    if settings.DEBUG and request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS:
        context_extras["debug"] = True
        from gingerdj.db import connections

        # Return a lazy reference that computes connection.queries on access,
        # to ensure it contains queries triggered after this function runs.
        context_extras["sql_queries"] = lazy(
            lambda: list(
                itertools.chain.from_iterable(
                    connections[x].queries for x in connections
                )
            ),
            list,
        )
    return context_extras


def i18n():
    """
    i18 support in context processor.
    """
    from gingerdj.utils import translation

    return {
        "LANGUAGES": settings.LANGUAGES,
        "LANGUAGE_CODE": translation.get_language(),
        "LANGUAGE_BIDI": translation.get_language_bidi(),
    }


def tz():
    """
    Timezone context processor.
    """
    from gingerdj.utils import timezone

    return {"TIME_ZONE": timezone.get_current_timezone_name()}


def static():
    """
    Add static-related context variables to the context.
    """
    return {"STATIC_URL": settings.STATIC_URL}


def media(request):
    """
    Add media-related context variables to the context.
    """
    return {"MEDIA_URL": settings.MEDIA_URL}


def request(request):
    return {"request": request}
