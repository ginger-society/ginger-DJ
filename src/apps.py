from ginger.apps import AppConfig


class SrcConfig(AppConfig):
    default_auto_field = 'ginger.db.models.BigAutoField'
    name = 'src'
