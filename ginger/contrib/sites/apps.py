from ginger.apps import AppConfig
from ginger.contrib.sites.checks import check_site_id
from ginger.core import checks
from ginger.db.models.signals import post_migrate
from ginger.utils.translation import gettext_lazy as _

from .management import create_default_site


class SitesConfig(AppConfig):
    default_auto_field = "ginger.db.models.AutoField"
    name = "ginger.contrib.sites"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_default_site, sender=self)
        checks.register(check_site_id, checks.Tags.sites)
