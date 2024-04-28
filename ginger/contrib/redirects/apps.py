from ginger.apps import AppConfig
from ginger.utils.translation import gettext_lazy as _


class RedirectsConfig(AppConfig):
    default_auto_field = "ginger.db.models.AutoField"
    name = "ginger.contrib.redirects"
    verbose_name = _("Redirects")
