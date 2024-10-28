from gingerdj.apps import AppConfig
from gingerdj.core import serializers
from gingerdj.utils.translation import gettext_lazy as _


class GISConfig(AppConfig):
    default_auto_field = "gingerdj.db.models.AutoField"
    name = "gingerdj.contrib.gis"
    verbose_name = _("GIS")

    def ready(self):
        serializers.BUILTIN_SERIALIZERS.setdefault(
            "geojson", "gingerdj.contrib.gis.serializers.geojson"
        )
