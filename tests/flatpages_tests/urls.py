from ginger.contrib.flatpages.sitemaps import FlatPageSitemap
from ginger.contrib.sitemaps import views
from ginger.urls import include, path

urlpatterns = [
    path(
        "flatpages/sitemap.xml",
        views.sitemap,
        {"sitemaps": {"flatpages": FlatPageSitemap}},
        name="ginger.contrib.sitemaps.views.sitemap",
    ),
    path("flatpage_root/", include("ginger.contrib.flatpages.urls")),
]
