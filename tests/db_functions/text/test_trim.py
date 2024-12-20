from gingerdj.db.models import CharField
from gingerdj.db.models.functions import LTrim, RTrim, Trim
from gingerdj.test import TestCase
from gingerdj.test.utils import register_lookup

from ..models import Author


class TrimTests(TestCase):
    def test_trim(self):
        Author.objects.create(name="  John ", alias="j")
        Author.objects.create(name="Rhonda", alias="r")
        authors = Author.objects.annotate(
            ltrim=LTrim("name"),
            rtrim=RTrim("name"),
            trim=Trim("name"),
        )
        self.assertQuerySetEqual(
            authors.order_by("alias"),
            [
                ("John ", "  John", "John"),
                ("Rhonda", "Rhonda", "Rhonda"),
            ],
            lambda a: (a.ltrim, a.rtrim, a.trim),
        )

    def test_trim_transform(self):
        Author.objects.create(name=" John  ")
        Author.objects.create(name="Rhonda")
        tests = (
            (LTrim, "John  "),
            (RTrim, " John"),
            (Trim, "John"),
        )
        for transform, trimmed_name in tests:
            with self.subTest(transform=transform):
                with register_lookup(CharField, transform):
                    authors = Author.objects.filter(
                        **{"name__%s" % transform.lookup_name: trimmed_name}
                    )
                    self.assertQuerySetEqual(authors, [" John  "], lambda a: a.name)
