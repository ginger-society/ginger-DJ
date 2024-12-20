from datetime import date, datetime, time

from gingerdj.forms import Form, SplitDateTimeField, SplitDateTimeWidget

from .base import WidgetTest


class SplitDateTimeWidgetTest(WidgetTest):
    widget = SplitDateTimeWidget()

    def test_render_empty(self):
        self.check_html(
            self.widget,
            "date",
            "",
            html=('<input type="text" name="date_0"><input type="text" name="date_1">'),
        )

    def test_render_none(self):
        self.check_html(
            self.widget,
            "date",
            None,
            html=('<input type="text" name="date_0"><input type="text" name="date_1">'),
        )

    def test_render_datetime(self):
        self.check_html(
            self.widget,
            "date",
            datetime(2006, 1, 10, 7, 30),
            html=(
                '<input type="text" name="date_0" value="2006-01-10">'
                '<input type="text" name="date_1" value="07:30:00">'
            ),
        )

    def test_render_date_and_time(self):
        self.check_html(
            self.widget,
            "date",
            [date(2006, 1, 10), time(7, 30)],
            html=(
                '<input type="text" name="date_0" value="2006-01-10">'
                '<input type="text" name="date_1" value="07:30:00">'
            ),
        )

    def test_constructor_attrs(self):
        widget = SplitDateTimeWidget(attrs={"class": "pretty"})
        self.check_html(
            widget,
            "date",
            datetime(2006, 1, 10, 7, 30),
            html=(
                '<input type="text" class="pretty" value="2006-01-10" name="date_0">'
                '<input type="text" class="pretty" value="07:30:00" name="date_1">'
            ),
        )

    def test_constructor_different_attrs(self):
        html = (
            '<input type="text" class="foo" value="2006-01-10" name="date_0">'
            '<input type="text" class="bar" value="07:30:00" name="date_1">'
        )
        widget = SplitDateTimeWidget(
            date_attrs={"class": "foo"}, time_attrs={"class": "bar"}
        )
        self.check_html(widget, "date", datetime(2006, 1, 10, 7, 30), html=html)
        widget = SplitDateTimeWidget(
            date_attrs={"class": "foo"}, attrs={"class": "bar"}
        )
        self.check_html(widget, "date", datetime(2006, 1, 10, 7, 30), html=html)
        widget = SplitDateTimeWidget(
            time_attrs={"class": "bar"}, attrs={"class": "foo"}
        )
        self.check_html(widget, "date", datetime(2006, 1, 10, 7, 30), html=html)

    def test_formatting(self):
        """
        Use 'date_format' and 'time_format' to change the way a value is
        displayed.
        """
        widget = SplitDateTimeWidget(
            date_format="%d/%m/%Y",
            time_format="%H:%M",
        )
        self.check_html(
            widget,
            "date",
            datetime(2006, 1, 10, 7, 30),
            html=(
                '<input type="text" name="date_0" value="10/01/2006">'
                '<input type="text" name="date_1" value="07:30">'
            ),
        )
        self.check_html(
            widget,
            "date",
            datetime(2006, 1, 10, 7, 30),
            html=(
                '<input type="text" name="date_0" value="10/01/2006">'
                '<input type="text" name="date_1" value="07:30">'
            ),
        )

    def test_fieldset(self):
        class TestForm(Form):
            template_name = "forms_tests/use_fieldset.html"
            field = SplitDateTimeField(widget=self.widget)

        form = TestForm()
        self.assertIs(self.widget.use_fieldset, True)
        self.assertHTMLEqual(
            '<div><fieldset><legend>Field:</legend><input type="text" '
            'name="field_0" required id="id_field_0"><input type="text" '
            'name="field_1" required id="id_field_1"></fieldset></div>',
            form.render(),
        )
