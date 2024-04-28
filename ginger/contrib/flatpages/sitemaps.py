from ginger.apps import apps as ginger_apps
from ginger.contrib.sitemaps import Sitemap
from ginger.core.exceptions import ImproperlyConfigured


class FlatPageSitemap(Sitemap):
    def items(self):
        if not ginger_apps.is_installed("ginger.contrib.sites"):
            raise ImproperlyConfigured(
                "FlatPageSitemap requires ginger.contrib.sites, which isn't installed."
            )
        Site = ginger_apps.get_model("sites.Site")
        current_site = Site.objects.get_current()
        return current_site.flatpage_set.filter(registration_required=False)
