from gingerdj.contrib.gis.db.backends.base.features import BaseSpatialFeatures
from gingerdj.db.backends.oracle.features import (
    DatabaseFeatures as OracleDatabaseFeatures,
)
from gingerdj.utils.functional import cached_property


class DatabaseFeatures(BaseSpatialFeatures, OracleDatabaseFeatures):
    supports_add_srs_entry = False
    supports_geometry_field_introspection = False
    supports_geometry_field_unique_index = False
    supports_perimeter_geodetic = True
    supports_dwithin_distance_expr = False
    supports_tolerance_parameter = True
    unsupported_geojson_options = {"bbox", "crs", "precision"}

    @cached_property
    def ginger_test_skips(self):
        skips = super().ginger_test_skips
        skips.update(
            {
                "Oracle doesn't support spatial operators in constraints.": {
                    "gis_tests.gis_migrations.test_operations.OperationTests."
                    "test_add_check_constraint",
                },
            }
        )
        return skips
