import datetime

from gingerdj.contrib.admin import ModelAdmin
from gingerdj.contrib.admin.templatetags.admin_list import date_hierarchy
from gingerdj.contrib.admin.templatetags.admin_modify import submit_row
from gingerdj.test import RequestFactory, TestCase
from gingerdj.urls import reverse

from .admin import ArticleAdmin, site
from .models import Article, Question
from .tests import AdminViewBasicTestCase, get_perm


class AdminTemplateTagsTest(AdminViewBasicTestCase):
    request_factory = RequestFactory()

    def test_submit_row(self):
        """
        submit_row template tag should pass whole context.
        """
        request = self.request_factory.get(
            reverse("admin:auth_user_change", args=[self.superuser.pk])
        )
        request.user = self.superuser
        extra_context = {"extra": True}

        template_context = submit_row(response.context_data)
        self.assertIs(template_context["extra"], True)
        self.assertIs(template_context["show_save"], True)

    def test_submit_row_save_as_new_add_permission_required(self):
        change_user = User.objects.create_user(
            username="change_user", password="secret", is_staff=True
        )
        change_user.user_permissions.add(
            get_perm(User, get_permission_codename("change", User._meta)),
        )
        request = self.request_factory.get(
            reverse("admin:auth_user_change", args=[self.superuser.pk])
        )
        request.user = change_user
        admin = UserAdmin(User, site)
        admin.save_as = True
        response = admin.change_view(request, str(self.superuser.pk))
        template_context = submit_row(response.context_data)
        self.assertIs(template_context["show_save_as_new"], False)

        add_user = User.objects.create_user(
            username="add_user", password="secret", is_staff=True
        )
        add_user.user_permissions.add(
            get_perm(User, get_permission_codename("add", User._meta)),
            get_perm(User, get_permission_codename("change", User._meta)),
        )
        request = self.request_factory.get(
            reverse("admin:auth_user_change", args=[self.superuser.pk])
        )
        request.user = add_user
        response = admin.change_view(request, str(self.superuser.pk))
        template_context = submit_row(response.context_data)
        self.assertIs(template_context["show_save_as_new"], True)

    def test_override_show_save_and_add_another(self):
        request = self.request_factory.get(
            reverse("admin:auth_user_change", args=[self.superuser.pk]),
        )
        request.user = self.superuser
        admin = UserAdmin(User, site)
        for extra_context, expected_flag in (
            ({}, True),  # Default.
            ({"show_save_and_add_another": False}, False),
        ):
            with self.subTest(show_save_and_add_another=expected_flag):
                response = admin.change_view(
                    request,
                    str(self.superuser.pk),
                    extra_context=extra_context,
                )
                template_context = submit_row(response.context_data)
                self.assertIs(
                    template_context["show_save_and_add_another"], expected_flag
                )

    def test_override_change_form_template_tags(self):
        """
        admin_modify template tags follow the standard search pattern
        admin/app_label/model/template.html.
        """
        article = Article.objects.all()[0]
        request = self.request_factory.get(
            reverse("admin:admin_views_article_change", args=[article.pk])
        )
        request.user = self.superuser
        admin = ArticleAdmin(Article, site)
        extra_context = {"show_publish": True, "extra": True}
        response = admin.change_view(
            request, str(article.pk), extra_context=extra_context
        )
        response.render()
        self.assertIs(response.context_data["show_publish"], True)
        self.assertIs(response.context_data["extra"], True)
        self.assertContains(response, 'name="_save"')
        self.assertContains(response, 'name="_publish"')
        self.assertContains(response, "override-change_form_object_tools")
        self.assertContains(response, "override-prepopulated_fields_js")

    def test_override_change_list_template_tags(self):
        """
        admin_list template tags follow the standard search pattern
        admin/app_label/model/template.html.
        """
        request = self.request_factory.get(
            reverse("admin:admin_views_article_changelist")
        )
        request.user = self.superuser
        admin = ArticleAdmin(Article, site)
        admin.date_hierarchy = "date"
        admin.search_fields = ("title", "content")
        response = admin.changelist_view(request)
        response.render()
        self.assertContains(response, "override-actions")
        self.assertContains(response, "override-change_list_object_tools")
        self.assertContains(response, "override-change_list_results")
        self.assertContains(response, "override-date_hierarchy")
        self.assertContains(response, "override-pagination")
        self.assertContains(response, "override-search_form")


class DateHierarchyTests(TestCase):
    factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User.objects.create_superuser(
            username="super", password="secret", email="super@example.com"
        )

    def test_choice_links(self):
        modeladmin = ModelAdmin(Question, site)
        modeladmin.date_hierarchy = "posted"

        posted_dates = (
            datetime.date(2017, 10, 1),
            datetime.date(2017, 10, 1),
            datetime.date(2017, 12, 15),
            datetime.date(2017, 12, 15),
            datetime.date(2017, 12, 31),
            datetime.date(2018, 2, 1),
        )
        Question.objects.bulk_create(
            Question(question="q", posted=posted) for posted in posted_dates
        )

        tests = (
            ({}, [["year=2017"], ["year=2018"]]),
            ({"year": 2016}, []),
            ({"year": 2017}, [["month=10", "year=2017"], ["month=12", "year=2017"]]),
            ({"year": 2017, "month": 9}, []),
            (
                {"year": 2017, "month": 12},
                [
                    ["day=15", "month=12", "year=2017"],
                    ["day=31", "month=12", "year=2017"],
                ],
            ),
        )
        for query, expected_choices in tests:
            with self.subTest(query=query):
                query = {"posted__%s" % q: val for q, val in query.items()}
                request = self.factory.get("/", query)
                request.user = self.superuser
                changelist = modeladmin.get_changelist_instance(request)
                spec = date_hierarchy(changelist)
                choices = [choice["link"] for choice in spec["choices"]]
                expected_choices = [
                    "&".join("posted__%s" % c for c in choice)
                    for choice in expected_choices
                ]
                expected_choices = [
                    ("?" + choice) if choice else "" for choice in expected_choices
                ]
                self.assertEqual(choices, expected_choices)

    def test_choice_links_datetime(self):
        modeladmin = ModelAdmin(Question, site)
        modeladmin.date_hierarchy = "expires"
        Question.objects.bulk_create(
            [
                Question(question="q1", expires=datetime.datetime(2017, 10, 1)),
                Question(question="q2", expires=datetime.datetime(2017, 10, 1)),
                Question(question="q3", expires=datetime.datetime(2017, 12, 15)),
                Question(question="q4", expires=datetime.datetime(2017, 12, 15)),
                Question(question="q5", expires=datetime.datetime(2017, 12, 31)),
                Question(question="q6", expires=datetime.datetime(2018, 2, 1)),
            ]
        )
        tests = [
            ({}, [["year=2017"], ["year=2018"]]),
            ({"year": 2016}, []),
            (
                {"year": 2017},
                [
                    ["month=10", "year=2017"],
                    ["month=12", "year=2017"],
                ],
            ),
            ({"year": 2017, "month": 9}, []),
            (
                {"year": 2017, "month": 12},
                [
                    ["day=15", "month=12", "year=2017"],
                    ["day=31", "month=12", "year=2017"],
                ],
            ),
        ]
        for query, expected_choices in tests:
            with self.subTest(query=query):
                query = {"expires__%s" % q: val for q, val in query.items()}
                request = self.factory.get("/", query)
                request.user = self.superuser
                changelist = modeladmin.get_changelist_instance(request)
                spec = date_hierarchy(changelist)
                choices = [choice["link"] for choice in spec["choices"]]
                expected_choices = [
                    "?" + "&".join("expires__%s" % c for c in choice)
                    for choice in expected_choices
                ]
                self.assertEqual(choices, expected_choices)
