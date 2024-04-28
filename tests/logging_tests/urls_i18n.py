from ginger.conf.urls.i18n import i18n_patterns
from ginger.http import HttpResponse
from ginger.urls import path

urlpatterns = i18n_patterns(
    path("exists/", lambda r: HttpResponse()),
)
