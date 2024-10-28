from gingerdj.urls import path, re_path
from gingerdj.utils.translation import gettext_lazy as _
from gingerdj.views.generic import TemplateView

view = TemplateView.as_view(template_name="dummy.html")

app_name = "account"
urlpatterns = [
    re_path(_(r"^register/$"), view, name="register"),
    re_path(_(r"^register-without-slash$"), view, name="register-without-slash"),
    path(_("register-as-path/"), view, name="register-as-path"),
]
