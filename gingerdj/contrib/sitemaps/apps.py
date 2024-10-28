from gingerdj.apps import AppConfig
from gingerdj.utils.translation import gettext_lazy as _


class SiteMapsConfig(AppConfig):
    default_auto_field = "gingerdj.db.models.AutoField"
    name = "gingerdj.contrib.sitemaps"
    verbose_name = _("Site Maps")
