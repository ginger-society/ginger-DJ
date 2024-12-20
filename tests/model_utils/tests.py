from gingerdj.db.models.utils import create_namedtuple_class
from gingerdj.test import SimpleTestCase


class NamedTupleClassTests(SimpleTestCase):
    def test_immutability(self):
        row_class = create_namedtuple_class("field1", "field2")
        row = row_class("value1", "value2")
        with self.assertRaises(AttributeError):
            row.field3 = "value3"
