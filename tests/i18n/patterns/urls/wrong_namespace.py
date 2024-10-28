from gingerdj.conf.urls.i18n import i18n_patterns
from gingerdj.urls import re_path
from gingerdj.utils.translation import gettext_lazy as _
from gingerdj.views.generic import TemplateView

view = TemplateView.as_view(template_name="dummy.html")

app_name = "account"
urlpatterns = i18n_patterns(
    re_path(_(r"^register/$"), view, name="register"),
)
