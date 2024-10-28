from gingerdj.conf.urls.i18n import i18n_patterns
from gingerdj.http import HttpResponse
from gingerdj.urls import path

urlpatterns = i18n_patterns(
    path("exists/", lambda r: HttpResponse()),
)
