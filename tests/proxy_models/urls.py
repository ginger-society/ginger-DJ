from ginger.urls import path

from .admin import site

urlpatterns = [
    path("admin/", site.urls),
]
