from gingerdj.conf.urls.i18n import i18n_patterns
from gingerdj.urls import path
from gingerdj.views.generic import TemplateView

view = TemplateView.as_view(template_name="dummy.html")

urlpatterns = i18n_patterns(
    path("prefixed/", view, name="prefixed"),
)
