from ginger.contrib.admin.helpers import ActionForm
from ginger.core.exceptions import ValidationError




class MediaActionForm(ActionForm):
    class Media:
        js = ["path/to/media.js"]
