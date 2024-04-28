from ginger.http import HttpResponse
from ginger.urls import path

urlpatterns = [
    path("", lambda request: HttpResponse("root is here")),
]
