from ginger.apps import AppConfig
from ginger.contrib.staticfiles.checks import check_finders, check_storages
from ginger.core import checks
from ginger.utils.translation import gettext_lazy as _


class StaticFilesConfig(AppConfig):
    name = "ginger.contrib.staticfiles"
    verbose_name = _("Static Files")
    ignore_patterns = ["CVS", ".*", "*~"]

    def ready(self):
        checks.register(check_finders, checks.Tags.staticfiles)
        checks.register(check_storages, checks.Tags.staticfiles)
