from gingerdj.apps import AppConfig
from gingerdj.utils.translation import gettext_lazy as _


class HumanizeConfig(AppConfig):
    name = "gingerdj.contrib.humanize"
    verbose_name = _("Humanize")
