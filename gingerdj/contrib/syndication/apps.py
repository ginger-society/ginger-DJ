from gingerdj.apps import AppConfig
from gingerdj.utils.translation import gettext_lazy as _


class SyndicationConfig(AppConfig):
    name = "gingerdj.contrib.syndication"
    verbose_name = _("Syndication")
