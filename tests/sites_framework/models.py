from gingerdj.contrib.sites.managers import CurrentSiteManager
from gingerdj.contrib.sites.models import Site
from gingerdj.db import models


class AbstractArticle(models.Model):
    title = models.CharField(max_length=50)

    objects = models.Manager()
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True


class SyndicatedArticle(AbstractArticle):
    sites = models.ManyToManyField(Site)


class ExclusiveArticle(AbstractArticle):
    site = models.ForeignKey(Site, models.CASCADE)


class CustomArticle(AbstractArticle):
    places_this_article_should_appear = models.ForeignKey(Site, models.CASCADE)

    objects = models.Manager()
    on_site = CurrentSiteManager("places_this_article_should_appear")
