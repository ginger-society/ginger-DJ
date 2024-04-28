import ginger
from ginger.core.handlers.asgi import ASGIHandler


def get_asgi_application():
    """
    The public interface to Ginger's ASGI support. Return an ASGI 3 callable.

    Avoids making ginger.core.handlers.ASGIHandler a public API, in case the
    internal implementation changes or moves in the future.
    """
    ginger.setup(set_prefix=False)
    return ASGIHandler()
