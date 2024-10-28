from gingerdj.conf.urls.i18n import i18n_patterns
from gingerdj.http import HttpResponse, StreamingHttpResponse
from gingerdj.urls import path
from gingerdj.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path("simple/", lambda r: HttpResponse()),
    path("streaming/", lambda r: StreamingHttpResponse([_("Yes"), "/", _("No")])),
)
