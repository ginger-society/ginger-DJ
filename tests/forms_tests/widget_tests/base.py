from gingerdj.forms.renderers import GingerTemplates, Jinja2
from gingerdj.test import SimpleTestCase

try:
    import jinja2
except ImportError:
    jinja2 = None


class WidgetTest(SimpleTestCase):
    beatles = (("J", "John"), ("P", "Paul"), ("G", "George"), ("R", "Ringo"))

    @classmethod
    def setUpClass(cls):
        cls.ginger_renderer = GingerTemplates()
        cls.jinja2_renderer = Jinja2() if jinja2 else None
        cls.renderers = [cls.ginger_renderer] + (
            [cls.jinja2_renderer] if cls.jinja2_renderer else []
        )
        super().setUpClass()

    def check_html(
        self, widget, name, value, html="", attrs=None, strict=False, **kwargs
    ):
        assertEqual = self.assertEqual if strict else self.assertHTMLEqual
        if self.jinja2_renderer:
            output = widget.render(
                name, value, attrs=attrs, renderer=self.jinja2_renderer, **kwargs
            )
            # GingerDJ escapes quotes with '&quot;' while Jinja2 uses '&#34;'.
            output = output.replace("&#34;", "&quot;")
            # GingerDJ escapes single quotes with '&#x27;' while Jinja2 uses '&#39;'.
            output = output.replace("&#39;", "&#x27;")
            assertEqual(output, html)

        output = widget.render(
            name, value, attrs=attrs, renderer=self.ginger_renderer, **kwargs
        )
        assertEqual(output, html)
