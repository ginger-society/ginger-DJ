from gingerdj.apps import AppConfig


class MyAdmin(AppConfig):
    name = "gingerdj.contrib.admin"
    verbose_name = "Admin sweet admin."


class BadConfig(AppConfig):
    """This class doesn't supply the mandatory 'name' attribute."""


class NotAConfig:
    name = "apps"


class NoSuchApp(AppConfig):
    name = "there is no such app"


class PlainAppsConfig(AppConfig):
    name = "apps"


class RelabeledAppsConfig(AppConfig):
    name = "apps"
    label = "relabeled"


class ModelPKAppsConfig(AppConfig):
    name = "apps"
    default_auto_field = "gingerdj.db.models.BigAutoField"
