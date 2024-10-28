from gingerdj.contrib import admin
from gingerdj.urls import include, path

urlpatterns = [
    path("admin/", include(admin.site.urls)),
]
