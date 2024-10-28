# RemovedInGinger60Warning: Remove this entire module.

from gingerdj.test import SimpleTestCase
from gingerdj.utils.deprecation import RemovedInGinger60Warning
from gingerdj.utils.itercompat import is_iterable


class TestIterCompat(SimpleTestCase):
    def test_is_iterable_deprecation(self):
        msg = (
            "gingerdj.utils.itercompat.is_iterable() is deprecated. "
            "Use isinstance(..., collections.abc.Iterable) instead."
        )
        with self.assertWarnsMessage(RemovedInGinger60Warning, msg):
            is_iterable([])
