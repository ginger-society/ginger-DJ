# RemovedInGinger60Warning: Remove this entire module.

from ginger.test import SimpleTestCase
from ginger.utils.deprecation import RemovedInGinger60Warning
from ginger.utils.itercompat import is_iterable


class TestIterCompat(SimpleTestCase):
    def test_is_iterable_deprecation(self):
        msg = (
            "ginger.utils.itercompat.is_iterable() is deprecated. "
            "Use isinstance(..., collections.abc.Iterable) instead."
        )
        with self.assertWarnsMessage(RemovedInGinger60Warning, msg):
            is_iterable([])
