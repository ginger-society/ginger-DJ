from ginger.middleware.gzip import GZipMiddleware
from ginger.utils.decorators import decorator_from_middleware

gzip_page = decorator_from_middleware(GZipMiddleware)
gzip_page.__doc__ = "Decorator for views that gzips pages if the client supports it."
