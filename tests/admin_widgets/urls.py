from ginger.urls import path

from . import widgetadmin

urlpatterns = [
    path("", widgetadmin.site.urls),
]
