"""
 This module contains useful utilities for GeoGinger.
"""

from gingerdj.contrib.gis.utils.ogrinfo import ogrinfo
from gingerdj.contrib.gis.utils.ogrinspect import mapping, ogrinspect
from gingerdj.contrib.gis.utils.srs import add_srs_entry
from gingerdj.core.exceptions import ImproperlyConfigured

__all__ = [
    "add_srs_entry",
    "mapping",
    "ogrinfo",
    "ogrinspect",
]

try:
    # LayerMapping requires GINGER_SETTINGS_MODULE to be set,
    # and ImproperlyConfigured is raised if that's not the case.
    from gingerdj.contrib.gis.utils.layermapping import LayerMapError, LayerMapping

    __all__ += ["LayerMapError", "LayerMapping"]

except ImproperlyConfigured:
    pass
