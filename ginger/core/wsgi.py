import ginger
from ginger.core.handlers.wsgi import WSGIHandler


def get_wsgi_application():
    """
    The public interface to Ginger's WSGI support. Return a WSGI callable.

    Avoids making ginger.core.handlers.WSGIHandler a public API, in case the
    internal WSGI implementation changes or moves in the future.
    """
    ginger.setup(set_prefix=False)
    return WSGIHandler()
