from ginger.urls import include, path

urlpatterns = [
    path("flatpage", include("ginger.contrib.flatpages.urls")),
]
