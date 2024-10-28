from gingerdj.contrib.flatpages.sitemaps import FlatPageSitemap
from gingerdj.contrib.sitemaps import views
from gingerdj.urls import include, path

urlpatterns = [
    path(
        "flatpages/sitemap.xml",
        views.sitemap,
        {"sitemaps": {"flatpages": FlatPageSitemap}},
        name="gingerdj.contrib.sitemaps.views.sitemap",
    ),
    path("flatpage_root/", include("gingerdj.contrib.flatpages.urls")),
]
