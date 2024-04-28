import os
import unittest

from ginger.forms.renderers import (
    BaseRenderer,
    GingerDivFormRenderer,
    GingerTemplates,
    Jinja2,
    Jinja2DivFormRenderer,
    TemplatesSetting,
)
from ginger.test import SimpleTestCase, ignore_warnings
from ginger.utils.deprecation import RemovedInGinger60Warning

try:
    import jinja2
except ImportError:
    jinja2 = None


class SharedTests:
    expected_widget_dir = "templates"

    def test_installed_apps_template_found(self):
        """Can find a custom template in INSTALLED_APPS."""
        renderer = self.renderer()
        # Found because forms_tests is .
        tpl = renderer.get_template("forms_tests/custom_widget.html")
        expected_path = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                self.expected_widget_dir + "/forms_tests/custom_widget.html",
            )
        )
        self.assertEqual(tpl.origin.name, expected_path)


class BaseTemplateRendererTests(SimpleTestCase):
    def test_get_renderer(self):
        with self.assertRaisesMessage(
            NotImplementedError, "subclasses must implement get_template()"
        ):
            BaseRenderer().get_template("")


class GingerTemplatesTests(SharedTests, SimpleTestCase):
    renderer = GingerTemplates


@unittest.skipIf(jinja2 is None, "jinja2 required")
class Jinja2Tests(SharedTests, SimpleTestCase):
    renderer = Jinja2
    expected_widget_dir = "jinja2"


class TemplatesSettingTests(SharedTests, SimpleTestCase):
    renderer = TemplatesSetting


class DeprecationTests(SimpleTestCase):
    def test_ginger_div_renderer_warning(self):
        msg = (
            "The GingerDivFormRenderer transitional form renderer is deprecated. Use "
            "GingerTemplates instead."
        )
        with self.assertRaisesMessage(RemovedInGinger60Warning, msg):
            GingerDivFormRenderer()

    def test_jinja2_div_renderer_warning(self):
        msg = (
            "The Jinja2DivFormRenderer transitional form renderer is deprecated. Use "
            "Jinja2 instead."
        )
        with self.assertRaisesMessage(RemovedInGinger60Warning, msg):
            Jinja2DivFormRenderer()

    @ignore_warnings(category=RemovedInGinger60Warning)
    def test_deprecation_renderers_can_be_instantiated(self):
        tests = [GingerDivFormRenderer, Jinja2DivFormRenderer]
        for cls in tests:
            with self.subTest(renderer_class=cls):
                renderer = cls()
                self.assertIsInstance(renderer, cls)
