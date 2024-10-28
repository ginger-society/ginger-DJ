from gingerdj.http import HttpResponse
from gingerdj.urls import path

urlpatterns = [
    path("", lambda request: HttpResponse("root is here")),
]
