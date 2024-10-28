from gingerdj.apps import AppConfig
from gingerdj.contrib.sites.checks import check_site_id
from gingerdj.core import checks
from gingerdj.db.models.signals import post_migrate
from gingerdj.utils.translation import gettext_lazy as _

from .management import create_default_site


class SitesConfig(AppConfig):
    default_auto_field = "gingerdj.db.models.AutoField"
    name = "gingerdj.contrib.sites"
    verbose_name = _("Sites")

    def ready(self):
        post_migrate.connect(create_default_site, sender=self)
        checks.register(check_site_id, checks.Tags.sites)
