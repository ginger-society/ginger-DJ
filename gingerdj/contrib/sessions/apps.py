from gingerdj.apps import AppConfig
from gingerdj.utils.translation import gettext_lazy as _


class SessionsConfig(AppConfig):
    name = "gingerdj.contrib.sessions"
    verbose_name = _("Sessions")
