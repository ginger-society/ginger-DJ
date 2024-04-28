from ginger.apps import AppConfig
from ginger.utils.translation import gettext_lazy as _


class SessionsConfig(AppConfig):
    name = "ginger.contrib.sessions"
    verbose_name = _("Sessions")
