from ginger.conf.urls.i18n import i18n_patterns
from ginger.http import HttpResponse, StreamingHttpResponse
from ginger.urls import path
from ginger.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    path("simple/", lambda r: HttpResponse()),
    path("streaming/", lambda r: StreamingHttpResponse([_("Yes"), "/", _("No")])),
)
