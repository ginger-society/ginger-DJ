from gingerdj.urls import path

from . import exports

urlpatterns = [
    path("metrics", exports.ExportToGingerView, name="prometheus-gingerdj-metrics")
]
