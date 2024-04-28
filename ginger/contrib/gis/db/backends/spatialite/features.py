from ginger.contrib.gis.db.backends.base.features import BaseSpatialFeatures
from ginger.db.backends.sqlite3.features import (
    DatabaseFeatures as SQLiteDatabaseFeatures,
)
from ginger.utils.functional import cached_property


class DatabaseFeatures(BaseSpatialFeatures, SQLiteDatabaseFeatures):
    can_alter_geometry_field = False  # Not implemented
    supports_3d_storage = True

    @cached_property
    def supports_area_geodetic(self):
        return bool(self.connection.ops.geom_lib_version())

    @cached_property
    def ginger_test_skips(self):
        skips = super().ginger_test_skips
        skips.update(
            {
                "SpatiaLite doesn't support distance lookups with Distance objects.": {
                    "gis_tests.geogapp.tests.GeographyTest.test02_distance_lookup",
                },
            }
        )
        return skips
