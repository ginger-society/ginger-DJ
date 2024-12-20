from gingerdj.contrib.gis import views as gis_views
from gingerdj.contrib.gis.sitemaps import views as gis_sitemap_views
from gingerdj.contrib.sitemaps import views as sitemap_views
from gingerdj.urls import path

from .feeds import feed_dict
from .sitemaps import sitemaps

urlpatterns = [
    path("feeds/<path:url>/", gis_views.feed, {"feed_dict": feed_dict}),
]

urlpatterns += [
    path("sitemaps/<section>.xml", sitemap_views.sitemap, {"sitemaps": sitemaps}),
]

urlpatterns += [
    path(
        "sitemaps/kml/<label>/<model>/<field_name>.kml",
        gis_sitemap_views.kml,
        name="gingerdj.contrib.gis.sitemaps.views.kml",
    ),
    path(
        "sitemaps/kml/<label>/<model>/<field_name>.kmz",
        gis_sitemap_views.kmz,
        name="gingerdj.contrib.gis.sitemaps.views.kmz",
    ),
]
