from ginger.apps import AppConfig
from ginger.utils.translation import gettext_lazy as _


class SyndicationConfig(AppConfig):
    name = "ginger.contrib.syndication"
    verbose_name = _("Syndication")
