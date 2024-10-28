from gingerdj.apps import AppConfig
from gingerdj.contrib.messages.storage import base
from gingerdj.contrib.messages.utils import get_level_tags
from gingerdj.core.signals import setting_changed
from gingerdj.utils.functional import SimpleLazyObject
from gingerdj.utils.translation import gettext_lazy as _


def update_level_tags(setting, **kwargs):
    if setting == "MESSAGE_TAGS":
        base.LEVEL_TAGS = SimpleLazyObject(get_level_tags)


class MessagesConfig(AppConfig):
    name = "gingerdj.contrib.messages"
    verbose_name = _("Messages")

    def ready(self):
        setting_changed.connect(update_level_tags)
