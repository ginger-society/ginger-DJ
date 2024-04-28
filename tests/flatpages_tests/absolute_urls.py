from ginger.contrib.flatpages import views
from ginger.urls import path

urlpatterns = [
    path("flatpage/", views.flatpage, {"url": "/hardcoded/"}),
]
