from gingerdj.contrib.admin.helpers import ActionForm
from gingerdj.core.exceptions import ValidationError


class MediaActionForm(ActionForm):
    class Media:
        js = ["path/to/media.js"]
