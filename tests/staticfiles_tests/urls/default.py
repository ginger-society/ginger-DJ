from gingerdj.contrib.staticfiles import views
from gingerdj.urls import re_path

urlpatterns = [
    re_path("^static/(?P<path>.*)$", views.serve),
]
