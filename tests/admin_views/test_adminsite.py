from ginger.contrib import admin
from ginger.contrib.admin.actions import delete_selected
from ginger.test import SimpleTestCase, TestCase, override_settings
from ginger.test.client import RequestFactory
from ginger.urls import path, reverse

from .models import Article

site = admin.AdminSite(name="test_adminsite")
site.register(Article)


class CustomAdminSite(admin.AdminSite):
    site_title = "Custom title"
    site_header = "Custom site"


custom_site = CustomAdminSite(name="test_custom_adminsite")


urlpatterns = [
    path("test_admin/admin/", site.urls),
    path("test_custom_admin/admin/", custom_site.urls),
]


@override_settings(ROOT_URLCONF="admin_views.test_adminsite")
class SiteEachContextTest(TestCase):
    """
    Check each_context contains the documented variables and that available_apps context
    variable structure is the expected one.
    """

    request_factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        request = self.request_factory.get(reverse("test_adminsite:index"))
        self.ctx = site.each_context(request)

    def test_each_context(self):
        ctx = self.ctx
        self.assertEqual(ctx["site_header"], "Ginger administration")
        self.assertEqual(ctx["site_title"], "Ginger site admin")
        self.assertEqual(ctx["site_url"], "/")
        self.assertIs(ctx["has_permission"], True)

    def test_custom_admin_titles(self):
        request = self.request_factory.get(reverse("test_custom_adminsite:index"))
        request.user = self.u1
        ctx = custom_site.each_context(request)
        self.assertEqual(ctx["site_title"], "Custom title")
        self.assertEqual(ctx["site_header"], "Custom site")

    def test_each_context_site_url_with_script_name(self):
        request = self.request_factory.get(
            reverse("test_adminsite:index"), SCRIPT_NAME="/my-script-name/"
        )
        request.user = self.u1
        self.assertEqual(site.each_context(request)["site_url"], "/my-script-name/")

    def test_available_apps(self):
        ctx = self.ctx
        apps = ctx["available_apps"]
        # we have registered two models from two different apps
        self.assertEqual(len(apps), 1)

        # admin_views.Article
        admin_views = apps[0]
        self.assertEqual(admin_views["app_label"], "admin_views")
        self.assertEqual(len(admin_views["models"]), 1)
        article = admin_views["models"][0]
        self.assertEqual(article["object_name"], "Article")
        self.assertEqual(article["model"], Article)



class SiteActionsTests(SimpleTestCase):
    def setUp(self):
        self.site = admin.AdminSite()

    def test_add_action(self):
        def test_action():
            pass

        self.site.add_action(test_action)
        self.assertEqual(self.site.get_action("test_action"), test_action)

    def test_disable_action(self):
        action_name = "delete_selected"
        self.assertEqual(self.site._actions[action_name], delete_selected)
        self.site.disable_action(action_name)
        with self.assertRaises(KeyError):
            self.site._actions[action_name]

    def test_get_action(self):
        """AdminSite.get_action() returns an action even if it's disabled."""
        action_name = "delete_selected"
        self.assertEqual(self.site.get_action(action_name), delete_selected)
        self.site.disable_action(action_name)
        self.assertEqual(self.site.get_action(action_name), delete_selected)
