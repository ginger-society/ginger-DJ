from ginger.contrib.staticfiles import views
from ginger.urls import re_path

urlpatterns = [
    re_path("^static/(?P<path>.*)$", views.serve),
]
