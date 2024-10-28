import gingerdj
from gingerdj.core.handlers.asgi import ASGIHandler


def get_asgi_application():
    """
    The public interface to GingerDJ's ASGI support. Return an ASGI 3 callable.

    Avoids making gingerdj.core.handlers.ASGIHandler a public API, in case the
    internal implementation changes or moves in the future.
    """
    gingerdj.setup(set_prefix=False)
    return ASGIHandler()
