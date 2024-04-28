try:
    from ginger.contrib.gis import admin
except ImportError:
    from ginger.contrib import admin

    admin.GISModelAdmin = admin.ModelAdmin
