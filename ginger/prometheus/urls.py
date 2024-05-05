from ginger.urls import path

from . import exports

urlpatterns = [path("metrics", exports.ExportToGingerView, name="prometheus-ginger-metrics")]
