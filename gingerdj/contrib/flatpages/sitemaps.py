from gingerdj.apps import apps as ginger_apps
from gingerdj.contrib.sitemaps import Sitemap
from gingerdj.core.exceptions import ImproperlyConfigured


class FlatPageSitemap(Sitemap):
    def items(self):
        if not ginger_apps.is_installed("gingerdj.contrib.sites"):
            raise ImproperlyConfigured(
                "FlatPageSitemap requires gingerdj.contrib.sites, which isn't installed."
            )
        Site = ginger_apps.get_model("sites.Site")
        current_site = Site.objects.get_current()
        return current_site.flatpage_set.filter(registration_required=False)
