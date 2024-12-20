from gingerdj.contrib.gis.db import models
from gingerdj.db import connection
from gingerdj.db.models import Index
from gingerdj.test import TransactionTestCase
from gingerdj.test.utils import isolate_apps

from .models import City


class SchemaIndexesTests(TransactionTestCase):
    available_apps = []
    models = [City]

    def get_indexes(self, table):
        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(cursor, table)
            return {
                name: constraint["columns"]
                for name, constraint in constraints.items()
                if constraint["index"]
            }

    def has_spatial_indexes(self, table):
        if connection.ops.mysql:
            with connection.cursor() as cursor:
                return connection.introspection.supports_spatial_index(cursor, table)
        elif connection.ops.oracle:
            # Spatial indexes in Meta.indexes are not supported by the Oracle
            # backend (see #31252).
            return False
        return True

    def test_using_sql(self):
        if not connection.ops.postgis:
            self.skipTest("This is a PostGIS-specific test.")
        index = Index(fields=["point"])
        editor = connection.schema_editor()
        self.assertIn(
            "%s USING " % editor.quote_name(City._meta.db_table),
            str(index.create_sql(City, editor)),
        )

    @isolate_apps("gis_tests.geoapp")
    def test_namespaced_db_table(self):
        if not connection.ops.postgis:
            self.skipTest("PostGIS-specific test.")

        class SchemaCity(models.Model):
            point = models.PointField()

            class Meta:
                app_label = "geoapp"
                db_table = 'ginger_schema"."geoapp_schema_city'

        index = Index(fields=["point"])
        editor = connection.schema_editor()
        create_index_sql = str(index.create_sql(SchemaCity, editor))
        self.assertIn(
            "%s USING " % editor.quote_name(SchemaCity._meta.db_table),
            create_index_sql,
        )
        self.assertIn(
            'CREATE INDEX "geoapp_schema_city_point_9ed70651_id" ',
            create_index_sql,
        )

    def test_index_name(self):
        if not self.has_spatial_indexes(City._meta.db_table):
            self.skipTest("Spatial indexes in Meta.indexes are not supported.")
        index_name = "custom_point_index_name"
        index = Index(fields=["point"], name=index_name)
        with connection.schema_editor() as editor:
            editor.add_index(City, index)
            indexes = self.get_indexes(City._meta.db_table)
            self.assertIn(index_name, indexes)
            self.assertEqual(indexes[index_name], ["point"])
            editor.remove_index(City, index)
