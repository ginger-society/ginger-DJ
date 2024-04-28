from ginger.contrib.flatpages import views
from ginger.urls import path

urlpatterns = [
    path("<path:url>", views.flatpage, name="ginger.contrib.flatpages.views.flatpage"),
]
