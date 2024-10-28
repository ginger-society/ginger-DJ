import gingerdj
from gingerdj.core.handlers.wsgi import WSGIHandler


def get_wsgi_application():
    """
    The public interface to GingerDJ's WSGI support. Return a WSGI callable.

    Avoids making gingerdj.core.handlers.WSGIHandler a public API, in case the
    internal WSGI implementation changes or moves in the future.
    """
    gingerdj.setup(set_prefix=False)
    return WSGIHandler()
