from gingerdj.urls import path
from gingerdj.views.generic import TemplateView

view = TemplateView.as_view(template_name="dummy.html")

urlpatterns = [
    path("foo/", view, name="not-prefixed-included-url"),
]
