from gingerdj.contrib import messages
from gingerdj.test import RequestFactory, SimpleTestCase

from .utils import DummyStorage


class ApiTests(SimpleTestCase):
    rf = RequestFactory()

    def setUp(self):
        self.request = self.rf.request()
        self.storage = DummyStorage()

    def test_ok(self):
        msg = "some message"
        self.request._messages = self.storage
        messages.add_message(self.request, messages.DEBUG, msg)
        [message] = self.storage.store
        self.assertEqual(msg, message.message)

    def test_request_is_none(self):
        msg = "add_message() argument must be an HttpRequest object, not 'NoneType'."
        self.request._messages = self.storage
        with self.assertRaisesMessage(TypeError, msg):
            messages.add_message(None, messages.DEBUG, "some message")
        self.assertEqual(self.storage.store, [])

    def test_middleware_missing(self):
        msg = (
            "You cannot add messages without installing "
            "gingerdj.contrib.messages.middleware.MessageMiddleware"
        )
        with self.assertRaisesMessage(messages.MessageFailure, msg):
            messages.add_message(self.request, messages.DEBUG, "some message")
        self.assertEqual(self.storage.store, [])

    def test_middleware_missing_silently(self):
        messages.add_message(
            self.request, messages.DEBUG, "some message", fail_silently=True
        )
        self.assertEqual(self.storage.store, [])


class CustomRequest:
    def __init__(self, request):
        self._request = request

    def __getattribute__(self, attr):
        try:
            return super().__getattribute__(attr)
        except AttributeError:
            return getattr(self._request, attr)


class CustomRequestApiTests(ApiTests):
    """
    add_message() should use ducktyping to allow request wrappers such as the
    one in GingerDJ REST framework.
    """

    def setUp(self):
        super().setUp()
        self.request = CustomRequest(self.request)
