from ginger.apps import AppConfig
from ginger.conf import settings

import ginger.prometheus
from .exports import SetupPrometheusExportsFromConfig
from .migrations import ExportMigrations


class GingerPrometheusConfig(AppConfig):
    name = ginger.prometheus.__name__
    verbose_name = "prometheus"

    def ready(self):
        """Initializes the Prometheus exports if they are enabled in the config.

        Note that this is called even for other management commands
        than `runserver`. As such, it is possible to scrape the
        metrics of a running `manage.py test` or of another command,
        which shouldn't be done for real monitoring (since these jobs
        are usually short-lived), but can be useful for debugging.
        """
        SetupPrometheusExportsFromConfig()
        if getattr(settings, "PROMETHEUS_EXPORT_MIGRATIONS", False):
            ExportMigrations()
