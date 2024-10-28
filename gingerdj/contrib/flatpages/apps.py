from gingerdj.apps import AppConfig
from gingerdj.utils.translation import gettext_lazy as _


class FlatPagesConfig(AppConfig):
    default_auto_field = "gingerdj.db.models.AutoField"
    name = "gingerdj.contrib.flatpages"
    verbose_name = _("Flat Pages")
