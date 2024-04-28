from ginger.http import HttpResponse
from ginger.urls import path


def empty_response(request):
    return HttpResponse()


urlpatterns = [
    path("middleware_urlconf_view/", empty_response, name="middleware_urlconf_view"),
]
