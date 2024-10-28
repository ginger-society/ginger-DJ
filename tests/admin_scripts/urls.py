import os

from gingerdj.urls import path
from gingerdj.views.static import serve

here = os.path.dirname(__file__)

urlpatterns = [
    path(
        "custom_templates/<path:path>",
        serve,
        {"document_root": os.path.join(here, "custom_templates")},
    ),
]
