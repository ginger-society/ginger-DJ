from gingerdj.contrib.flatpages import views
from gingerdj.urls import path

urlpatterns = [
    path("flatpage/", views.flatpage, {"url": "/hardcoded/"}),
]
