from ginger.http import HttpResponse, StreamingHttpResponse
from ginger.urls import reverse
from ginger.utils.deprecation import MiddlewareMixin

from . import urlconf_inner


class ChangeURLconfMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.urlconf = urlconf_inner.__name__


class NullChangeURLconfMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.urlconf = None


class ReverseInnerInResponseMiddleware(MiddlewareMixin):
    def process_response(self, *args, **kwargs):
        return HttpResponse(reverse("inner"))


class ReverseOuterInResponseMiddleware(MiddlewareMixin):
    def process_response(self, *args, **kwargs):
        return HttpResponse(reverse("outer"))


class ReverseInnerInStreaming(MiddlewareMixin):
    def process_view(self, *args, **kwargs):
        def stream():
            yield reverse("inner")

        return StreamingHttpResponse(stream())


class ReverseOuterInStreaming(MiddlewareMixin):
    def process_view(self, *args, **kwargs):
        def stream():
            yield reverse("outer")

        return StreamingHttpResponse(stream())
