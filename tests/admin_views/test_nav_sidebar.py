from ginger.contrib import admin
from ginger.contrib.admin.tests import AdminSeleniumTestCase
from ginger.test import TestCase, override_settings
from ginger.urls import path, reverse

from .models import Héllo


class AdminSiteWithSidebar(admin.AdminSite):
    pass


class AdminSiteWithoutSidebar(admin.AdminSite):
    enable_nav_sidebar = False


site_with_sidebar = AdminSiteWithSidebar(name="test_with_sidebar")
site_without_sidebar = AdminSiteWithoutSidebar(name="test_without_sidebar")

site_with_sidebar.register(Héllo)

urlpatterns = [
    path("test_sidebar/admin/", site_with_sidebar.urls),
    path("test_wihout_sidebar/admin/", site_without_sidebar.urls),
]


@override_settings(ROOT_URLCONF="admin_views.test_nav_sidebar")
class AdminSidebarTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        # self.client.force_login(self.superuser)
        pass

    def test_sidebar_not_on_index(self):
        response = self.client.get(reverse("test_with_sidebar:index"))
        self.assertContains(response, '<div class="main" id="main">')
        self.assertNotContains(
            response, '<nav class="sticky" id="nav-sidebar" aria-label="Sidebar">'
        )

    def test_sidebar_disabled(self):
        response = self.client.get(reverse("test_without_sidebar:index"))
        self.assertNotContains(
            response, '<nav class="sticky" id="nav-sidebar" aria-label="Sidebar">'
        )

    @override_settings(
        TEMPLATES=[
            {
                "BACKEND": "ginger.template.backends.ginger.GingerTemplates",
                "DIRS": [],
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "ginger.contrib.messages.context_processors.messages",
                    ],
                },
            }
        ]
    )

    def test_sidebar_model_name_non_ascii(self):
        url = reverse("test_with_sidebar:admin_views_héllo_changelist")
        response = self.client.get(url)
        self.assertContains(
            response, 'Start typing to filter'
        )
        self.assertContains(response, 'admin_views-héllo')


@override_settings(ROOT_URLCONF="admin_views.test_nav_sidebar")
class SeleniumTests(AdminSeleniumTestCase):
    available_apps = ["admin_views"] + AdminSeleniumTestCase.available_apps

    def setUp(self):
        self.selenium.execute_script(
            "localStorage.removeItem('ginger.admin.navSidebarIsOpen')"
        )

    def test_sidebar_starts_open(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url + reverse("test_with_sidebar:auth_user_changelist")
        )
        main_element = self.selenium.find_element(By.CSS_SELECTOR, "#main")
        self.assertIn("shifted", main_element.get_attribute("class").split())

    def test_sidebar_can_be_closed(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url + reverse("test_with_sidebar:auth_user_changelist")
        )
        toggle_button = self.selenium.find_element(
            By.CSS_SELECTOR, "#toggle-nav-sidebar"
        )
        self.assertEqual(toggle_button.tag_name, "button")
        self.assertEqual(toggle_button.get_attribute("aria-label"), "Toggle navigation")
        nav_sidebar = self.selenium.find_element(By.ID, "nav-sidebar")
        self.assertEqual(nav_sidebar.get_attribute("aria-expanded"), "true")
        self.assertTrue(nav_sidebar.is_displayed())
        toggle_button.click()

        # Hidden sidebar is not visible.
        nav_sidebar = self.selenium.find_element(By.ID, "nav-sidebar")
        self.assertEqual(nav_sidebar.get_attribute("aria-expanded"), "false")
        self.assertFalse(nav_sidebar.is_displayed())
        main_element = self.selenium.find_element(By.CSS_SELECTOR, "#main")
        self.assertNotIn("shifted", main_element.get_attribute("class").split())

    def test_sidebar_state_persists(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url + reverse("test_with_sidebar:auth_user_changelist")
        )
        self.assertIsNone(
            self.selenium.execute_script(
                "return localStorage.getItem('ginger.admin.navSidebarIsOpen')"
            )
        )
        toggle_button = self.selenium.find_element(
            By.CSS_SELECTOR, "#toggle-nav-sidebar"
        )
        toggle_button.click()
        self.assertEqual(
            self.selenium.execute_script(
                "return localStorage.getItem('ginger.admin.navSidebarIsOpen')"
            ),
            "false",
        )
        self.selenium.get(
            self.live_server_url + reverse("test_with_sidebar:auth_user_changelist")
        )
        main_element = self.selenium.find_element(By.CSS_SELECTOR, "#main")
        self.assertNotIn("shifted", main_element.get_attribute("class").split())

        toggle_button = self.selenium.find_element(
            By.CSS_SELECTOR, "#toggle-nav-sidebar"
        )
        # Hidden sidebar is not visible.
        nav_sidebar = self.selenium.find_element(By.ID, "nav-sidebar")
        self.assertEqual(nav_sidebar.get_attribute("aria-expanded"), "false")
        self.assertFalse(nav_sidebar.is_displayed())
        toggle_button.click()
        nav_sidebar = self.selenium.find_element(By.ID, "nav-sidebar")
        self.assertEqual(nav_sidebar.get_attribute("aria-expanded"), "true")
        self.assertTrue(nav_sidebar.is_displayed())
        self.assertEqual(
            self.selenium.execute_script(
                "return localStorage.getItem('ginger.admin.navSidebarIsOpen')"
            ),
            "true",
        )
        self.selenium.get(
            self.live_server_url + reverse("test_with_sidebar:auth_user_changelist")
        )
        main_element = self.selenium.find_element(By.CSS_SELECTOR, "#main")
        self.assertIn("shifted", main_element.get_attribute("class").split())

    def test_sidebar_filter_persists(self):
        from selenium.webdriver.common.by import By

        self.selenium.get(
            self.live_server_url + reverse("test_with_sidebar:auth_user_changelist")
        )
        filter_value_script = (
            "return sessionStorage.getItem('ginger.admin.navSidebarFilterValue')"
        )
        self.assertIsNone(self.selenium.execute_script(filter_value_script))
        filter_input = self.selenium.find_element(By.CSS_SELECTOR, "#nav-filter")
        filter_input.send_keys("users")
        self.assertEqual(self.selenium.execute_script(filter_value_script), "users")
