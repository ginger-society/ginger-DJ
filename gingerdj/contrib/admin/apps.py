from gingerdj.apps import AppConfig
from gingerdj.contrib.admin.checks import check_admin_app, check_dependencies
from gingerdj.core import checks
from gingerdj.utils.translation import gettext_lazy as _


class SimpleAdminConfig(AppConfig):
    """Simple AppConfig which does not do automatic discovery."""

    default_auto_field = "gingerdj.db.models.AutoField"
    default_site = "gingerdj.contrib.admin.sites.AdminSite"
    name = "gingerdj.contrib.admin"
    verbose_name = _("Administration")

    def ready(self):
        checks.register(check_dependencies, checks.Tags.admin)
        checks.register(check_admin_app, checks.Tags.admin)


class AdminConfig(SimpleAdminConfig):
    """The default AppConfig for admin which does autodiscovery."""

    default = True

    def ready(self):
        super().ready()
        self.module.autodiscover()
