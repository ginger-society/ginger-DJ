from gingerdj.contrib.flatpages import views
from gingerdj.urls import path

urlpatterns = [
    path(
        "<path:url>", views.flatpage, name="gingerdj.contrib.flatpages.views.flatpage"
    ),
]
