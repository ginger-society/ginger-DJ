from ginger.http import HttpResponse
from ginger.urls import path

urlpatterns = [
    path("", lambda req: HttpResponse("OK")),
]
