from gingerdj.urls import path

from . import views

urlpatterns = [
    path("fileresponse/", views.file_response),
]
