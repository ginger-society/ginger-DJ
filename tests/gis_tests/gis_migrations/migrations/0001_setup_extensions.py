from gingerdj.db import connection, migrations

if connection.features.supports_raster:
    from gingerdj.contrib.postgres.operations import CreateExtension

    class Migration(migrations.Migration):
        operations = [
            CreateExtension("postgis_raster"),
        ]

else:

    class Migration(migrations.Migration):
        operations = []
