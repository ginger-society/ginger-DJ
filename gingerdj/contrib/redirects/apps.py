from gingerdj.apps import AppConfig
from gingerdj.utils.translation import gettext_lazy as _


class RedirectsConfig(AppConfig):
    default_auto_field = "gingerdj.db.models.AutoField"
    name = "gingerdj.contrib.redirects"
    verbose_name = _("Redirects")
