from ginger.apps import AppConfig
from ginger.core import serializers
from ginger.utils.translation import gettext_lazy as _


class GISConfig(AppConfig):
    default_auto_field = "ginger.db.models.AutoField"
    name = "ginger.contrib.gis"
    verbose_name = _("GIS")

    def ready(self):
        serializers.BUILTIN_SERIALIZERS.setdefault(
            "geojson", "ginger.contrib.gis.serializers.geojson"
        )
