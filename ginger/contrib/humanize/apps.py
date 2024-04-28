from ginger.apps import AppConfig
from ginger.utils.translation import gettext_lazy as _


class HumanizeConfig(AppConfig):
    name = "ginger.contrib.humanize"
    verbose_name = _("Humanize")
