"""
 This module contains useful utilities for GeoGinger.
"""

from ginger.contrib.gis.utils.ogrinfo import ogrinfo
from ginger.contrib.gis.utils.ogrinspect import mapping, ogrinspect
from ginger.contrib.gis.utils.srs import add_srs_entry
from ginger.core.exceptions import ImproperlyConfigured

__all__ = [
    "add_srs_entry",
    "mapping",
    "ogrinfo",
    "ogrinspect",
]

try:
    # LayerMapping requires GINGER_SETTINGS_MODULE to be set,
    # and ImproperlyConfigured is raised if that's not the case.
    from ginger.contrib.gis.utils.layermapping import LayerMapError, LayerMapping

    __all__ += ["LayerMapError", "LayerMapping"]

except ImproperlyConfigured:
    pass
