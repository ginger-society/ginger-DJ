from gingerdj.db import models
from gingerdj.db.backends.base.schema import BaseDatabaseSchemaEditor
from gingerdj.test import SimpleTestCase


class SchemaEditorTests(SimpleTestCase):
    def test_effective_default_callable(self):
        """SchemaEditor.effective_default() shouldn't call callable defaults."""

        class MyStr(str):
            def __call__(self):
                return self

        class MyCharField(models.CharField):
            def _get_default(self):
                return self.default

        field = MyCharField(max_length=1, default=MyStr)
        self.assertEqual(BaseDatabaseSchemaEditor._effective_default(field), MyStr)
