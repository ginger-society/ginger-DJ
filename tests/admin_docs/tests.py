from gingerdj.test import SimpleTestCase, TestCase, modify_settings, override_settings


class TestDataMixin:
    @classmethod
    def setUpTestData(cls):
        pass


@override_settings(ROOT_URLCONF="admin_docs.urls")
@modify_settings(INSTALLED_APPS={"append": "gingerdj.contrib.admindocs"})
class AdminDocsSimpleTestCase(SimpleTestCase):
    pass


@override_settings(ROOT_URLCONF="admin_docs.urls")
@modify_settings(INSTALLED_APPS={"append": "gingerdj.contrib.admindocs"})
class AdminDocsTestCase(TestCase):
    pass
