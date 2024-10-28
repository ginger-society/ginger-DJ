from gingerdj.conf.urls.i18n import i18n_patterns
from gingerdj.http import HttpResponse
from gingerdj.urls import path, re_path
from gingerdj.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    re_path(r"^(?P<arg>[\w-]+)-page", lambda request, **arg: HttpResponse(_("Yes"))),
    path("simple/", lambda r: HttpResponse(_("Yes"))),
    re_path(r"^(.+)/(.+)/$", lambda *args: HttpResponse()),
    re_path(_(r"^users/$"), lambda *args: HttpResponse(), name="users"),
    prefix_default_language=False,
)
