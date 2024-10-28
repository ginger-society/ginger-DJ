try:
    from gingerdj.contrib.gis import admin
except ImportError:
    from gingerdj.contrib import admin

    admin.GISModelAdmin = admin.ModelAdmin
