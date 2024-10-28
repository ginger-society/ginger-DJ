from gingerdj.apps import AppConfig
from gingerdj.conf import settings

import gingerdj.prometheus
from .exports import SetupPrometheusExportsFromConfig
from .migrations import ExportMigrations


class GingerPrometheusConfig(AppConfig):
    name = gingerdj.prometheus.__name__
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
