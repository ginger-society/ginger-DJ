from ginger.apps import AppConfig
from ginger.contrib.messages.storage import base
from ginger.contrib.messages.utils import get_level_tags
from ginger.core.signals import setting_changed
from ginger.utils.functional import SimpleLazyObject
from ginger.utils.translation import gettext_lazy as _


def update_level_tags(setting, **kwargs):
    if setting == "MESSAGE_TAGS":
        base.LEVEL_TAGS = SimpleLazyObject(get_level_tags)


class MessagesConfig(AppConfig):
    name = "ginger.contrib.messages"
    verbose_name = _("Messages")

    def ready(self):
        setting_changed.connect(update_level_tags)
