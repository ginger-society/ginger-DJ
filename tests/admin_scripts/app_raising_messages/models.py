from ginger.core import checks
from ginger.db import models


class ModelRaisingMessages(models.Model):
    @classmethod
    def check(self, **kwargs):
        return [
            checks.Warning("First warning", hint="Hint", obj="obj"),
            checks.Warning("Second warning", obj="a"),
            checks.Error("An error", hint="Error hint"),
        ]
