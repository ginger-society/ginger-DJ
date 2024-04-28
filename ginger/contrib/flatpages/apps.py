from ginger.apps import AppConfig
from ginger.utils.translation import gettext_lazy as _


class FlatPagesConfig(AppConfig):
    default_auto_field = "ginger.db.models.AutoField"
    name = "ginger.contrib.flatpages"
    verbose_name = _("Flat Pages")
