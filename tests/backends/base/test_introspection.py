from gingerdj.db import connection
from gingerdj.db.backends.base.introspection import BaseDatabaseIntrospection
from gingerdj.test import SimpleTestCase


class SimpleDatabaseIntrospectionTests(SimpleTestCase):
    may_require_msg = (
        "subclasses of BaseDatabaseIntrospection may require a %s() method"
    )

    def setUp(self):
        self.introspection = BaseDatabaseIntrospection(connection=connection)

    def test_get_table_list(self):
        msg = self.may_require_msg % "get_table_list"
        with self.assertRaisesMessage(NotImplementedError, msg):
            self.introspection.get_table_list(None)

    def test_get_table_description(self):
        msg = self.may_require_msg % "get_table_description"
        with self.assertRaisesMessage(NotImplementedError, msg):
            self.introspection.get_table_description(None, None)

    def test_get_sequences(self):
        msg = self.may_require_msg % "get_sequences"
        with self.assertRaisesMessage(NotImplementedError, msg):
            self.introspection.get_sequences(None, None)

    def test_get_relations(self):
        msg = self.may_require_msg % "get_relations"
        with self.assertRaisesMessage(NotImplementedError, msg):
            self.introspection.get_relations(None, None)

    def test_get_constraints(self):
        msg = self.may_require_msg % "get_constraints"
        with self.assertRaisesMessage(NotImplementedError, msg):
            self.introspection.get_constraints(None, None)
