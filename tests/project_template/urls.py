from ginger.urls import path

from . import views

urlpatterns = [
    path("empty/", views.empty_view),
]
