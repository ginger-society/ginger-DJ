from ginger.contrib import admin
from ginger.urls import include, path

urlpatterns = [
    path("admin/", include(admin.site.urls)),
]
