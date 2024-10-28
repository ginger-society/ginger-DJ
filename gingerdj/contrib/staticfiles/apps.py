from gingerdj.apps import AppConfig
from gingerdj.contrib.staticfiles.checks import check_finders, check_storages
from gingerdj.core import checks
from gingerdj.utils.translation import gettext_lazy as _


class StaticFilesConfig(AppConfig):
    name = "gingerdj.contrib.staticfiles"
    verbose_name = _("Static Files")
    ignore_patterns = ["CVS", ".*", "*~"]

    def ready(self):
        checks.register(check_finders, checks.Tags.staticfiles)
        checks.register(check_storages, checks.Tags.staticfiles)
