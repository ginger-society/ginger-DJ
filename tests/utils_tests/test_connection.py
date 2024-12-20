from gingerdj.test import SimpleTestCase
from gingerdj.utils.connection import BaseConnectionHandler


class BaseConnectionHandlerTests(SimpleTestCase):
    def test_create_connection(self):
        handler = BaseConnectionHandler()
        msg = "Subclasses must implement create_connection()."
        with self.assertRaisesMessage(NotImplementedError, msg):
            handler.create_connection(None)

    def test_all_initialized_only(self):
        handler = BaseConnectionHandler({"default": {}})
        self.assertEqual(handler.all(initialized_only=True), [])
