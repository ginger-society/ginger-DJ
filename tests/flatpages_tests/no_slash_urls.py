from gingerdj.urls import include, path

urlpatterns = [
    path("flatpage", include("gingerdj.contrib.flatpages.urls")),
]
