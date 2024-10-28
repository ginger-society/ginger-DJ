from gingerdj.http import HttpResponse
from gingerdj.urls import path

urlpatterns = [
    path("", lambda req: HttpResponse("OK")),
]
