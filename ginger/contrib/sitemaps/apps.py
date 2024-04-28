from ginger.apps import AppConfig
from ginger.utils.translation import gettext_lazy as _


class SiteMapsConfig(AppConfig):
    default_auto_field = "ginger.db.models.AutoField"
    name = "ginger.contrib.sitemaps"
    verbose_name = _("Site Maps")
