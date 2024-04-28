from ginger.conf.urls.i18n import i18n_patterns
from ginger.http import HttpResponse
from ginger.urls import path, re_path
from ginger.utils.translation import gettext_lazy as _

urlpatterns = i18n_patterns(
    re_path(r"^(?P<arg>[\w-]+)-page", lambda request, **arg: HttpResponse(_("Yes"))),
    path("simple/", lambda r: HttpResponse(_("Yes"))),
    re_path(r"^(.+)/(.+)/$", lambda *args: HttpResponse()),
    re_path(_(r"^users/$"), lambda *args: HttpResponse(), name="users"),
    prefix_default_language=False,
)
