from unittest import TestCase

from ginger.test import SimpleTestCase
from ginger.test import TestCase as GingerTestCase


class GingerCase1(GingerTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class GingerCase2(GingerTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class SimpleCase1(SimpleTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class SimpleCase2(SimpleTestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class UnittestCase1(TestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass


class UnittestCase2(TestCase):
    def test_1(self):
        pass

    def test_2(self):
        pass

    def test_3_test(self):
        pass
