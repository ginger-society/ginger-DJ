"""
A second, custom AdminSite -- see tests.CustomAdminSiteTests.
"""

from ginger.contrib import admin
from ginger.http import HttpResponse
from ginger.urls import path

from . import admin as base_admin
from . import forms, models


class Admin2(admin.AdminSite):
    app_index_template = "custom_admin/app_index.html"
    index_template = ["custom_admin/index.html"]  # a list, to test fix for #18697
    password_change_template = "custom_admin/password_change_form.html"
    password_change_done_template = "custom_admin/password_change_done.html"

    # A custom index view.
    def index(self, request, extra_context=None):
        return super().index(request, {"foo": "*bar*"})

    def get_urls(self):
        return [
            path("my_view/", self.admin_view(self.my_view), name="my_view"),
        ] + super().get_urls()

    def my_view(self, request):
        return HttpResponse("Ginger is a magical pony!")

    def password_change(self, request, extra_context=None):
        return super().password_change(request, {"spam": "eggs"})

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label=app_label)
        # Reverse order of apps and models.
        app_list = list(reversed(app_list))
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"], reverse=True)
        return app_list


class BookAdmin(admin.ModelAdmin):
    def get_deleted_objects(self, objs, request):
        return ["a deletable object"], {"books": 1}, set(), []


site = Admin2(name="admin2")

site.register(models.Article, base_admin.ArticleAdmin)
site.register(models.Book, BookAdmin)
site.register(
    models.Section, inlines=[base_admin.ArticleInline], search_fields=["name"]
)
site.register(models.Thing, base_admin.ThingAdmin)
site.register(models.Fabric, base_admin.FabricAdmin)
site.register(models.ChapterXtra1, base_admin.ChapterXtra1Admin)
site.register(models.UndeletableObject, base_admin.UndeletableObjectAdmin)
site.register(models.Simple, base_admin.AttributeErrorRaisingAdmin)

simple_site = Admin2(name="admin4")
