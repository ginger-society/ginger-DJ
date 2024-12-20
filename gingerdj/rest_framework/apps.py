from gingerdj.apps import AppConfig


class RestFrameworkConfig(AppConfig):
    name = "gingerdj.rest_framework"
    verbose_name = "Django REST framework"

    def ready(self):
        # Add System checks
        from .checks import pagination_system_check  # NOQA
