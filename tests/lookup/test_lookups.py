from datetime import datetime
from unittest import mock

from gingerdj.db.models import DateTimeField, Value
from gingerdj.db.models.lookups import Lookup, YearLookup
from gingerdj.test import SimpleTestCase


class CustomLookup(Lookup):
    pass


class LookupTests(SimpleTestCase):
    def test_equality(self):
        lookup = Lookup(Value(1), Value(2))
        self.assertEqual(lookup, lookup)
        self.assertEqual(lookup, Lookup(lookup.lhs, lookup.rhs))
        self.assertEqual(lookup, mock.ANY)
        self.assertNotEqual(lookup, Lookup(lookup.lhs, Value(3)))
        self.assertNotEqual(lookup, Lookup(Value(3), lookup.rhs))
        self.assertNotEqual(lookup, CustomLookup(lookup.lhs, lookup.rhs))

    def test_repr(self):
        tests = [
            (Lookup(Value(1), Value("a")), "Lookup(Value(1), Value('a'))"),
            (
                YearLookup(
                    Value(datetime(2010, 1, 1, 0, 0, 0)),
                    Value(datetime(2010, 1, 1, 23, 59, 59)),
                ),
                "YearLookup("
                "Value(datetime.datetime(2010, 1, 1, 0, 0)), "
                "Value(datetime.datetime(2010, 1, 1, 23, 59, 59)))",
            ),
        ]
        for lookup, expected in tests:
            with self.subTest(lookup=lookup):
                self.assertEqual(repr(lookup), expected)

    def test_hash(self):
        lookup = Lookup(Value(1), Value(2))
        self.assertEqual(hash(lookup), hash(lookup))
        self.assertEqual(hash(lookup), hash(Lookup(lookup.lhs, lookup.rhs)))
        self.assertNotEqual(hash(lookup), hash(Lookup(lookup.lhs, Value(3))))
        self.assertNotEqual(hash(lookup), hash(Lookup(Value(3), lookup.rhs)))
        self.assertNotEqual(hash(lookup), hash(CustomLookup(lookup.lhs, lookup.rhs)))


class YearLookupTests(SimpleTestCase):
    def test_get_bound_params(self):
        look_up = YearLookup(
            lhs=Value(datetime(2010, 1, 1, 0, 0, 0), output_field=DateTimeField()),
            rhs=Value(datetime(2010, 1, 1, 23, 59, 59), output_field=DateTimeField()),
        )
        msg = "subclasses of YearLookup must provide a get_bound_params() method"
        with self.assertRaisesMessage(NotImplementedError, msg):
            look_up.get_bound_params(
                datetime(2010, 1, 1, 0, 0, 0), datetime(2010, 1, 1, 23, 59, 59)
            )
