from functools import update_wrapper
from weakref import WeakSet

from ginger.apps import apps
from ginger.conf import settings
from ginger.contrib.admin import ModelAdmin, actions
from ginger.contrib.admin.exceptions import AlreadyRegistered, NotRegistered
from ginger.contrib.admin.views.autocomplete import AutocompleteJsonView
from ginger.core.exceptions import ImproperlyConfigured
from ginger.db.models.base import ModelBase
from ginger.http import Http404, HttpResponsePermanentRedirect, HttpResponseRedirect
from ginger.template.response import TemplateResponse
from ginger.urls import NoReverseMatch, Resolver404, resolve, reverse
from ginger.utils.decorators import method_decorator
from ginger.utils.functional import LazyObject
from ginger.utils.module_loading import import_string
from ginger.utils.text import capfirst
from ginger.utils.translation import gettext as _
from ginger.utils.translation import gettext_lazy
from ginger.views.decorators.cache import never_cache
from ginger.views.decorators.common import no_append_slash
from ginger.views.decorators.csrf import csrf_protect
from ginger.views.i18n import JavaScriptCatalog

all_sites = WeakSet()


class AdminSite:
    """
    An AdminSite object encapsulates an instance of the Ginger admin application, ready
    to be hooked in to your URLconf. Models are registered with the AdminSite using the
    register() method, and the get_urls() method can then be used to access Ginger view
    functions that present a full admin interface for the collection of registered
    models.
    """

    # Text to put at the end of each page's <title>.
    site_title = gettext_lazy("Ginger site admin")

    # Text to put in each page's <div id="site-name">.
    site_header = gettext_lazy("Ginger administration")

    # Text to put at the top of the admin index page.
    index_title = gettext_lazy("Site administration")

    # URL for the "View site" link at the top of each admin page.
    site_url = "/"

    enable_nav_sidebar = True

    empty_value_display = "-"

    login_form = None
    index_template = None
    app_index_template = None
    login_template = None
    logout_template = None
    password_change_template = None
    password_change_done_template = None

    final_catch_all_view = True

    def __init__(self, name="admin"):
        self._registry = {}  # model_class class -> admin_class instance
        self.name = name
        self._actions = {"delete_selected": actions.delete_selected}
        self._global_actions = self._actions.copy()
        all_sites.add(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"

    def check(self, app_configs):
        """
        Run the system checks on all ModelAdmins, except if they aren't
        customized at all.
        """
        if app_configs is None:
            app_configs = apps.get_app_configs()
        app_configs = set(app_configs)  # Speed up lookups below

        errors = []
        modeladmins = (
            o for o in self._registry.values() if o.__class__ is not ModelAdmin
        )
        for modeladmin in modeladmins:
            if modeladmin.model._meta.app_config in app_configs:
                errors.extend(modeladmin.check())
        return errors

    def register(self, model_or_iterable, admin_class=None, **options):
        """
        Register the given model(s) with the given admin class.

        The model(s) should be Model classes, not instances.

        If an admin class isn't given, use ModelAdmin (the default admin
        options). If keyword arguments are given -- e.g., list_display --
        apply them as options to the admin class.

        If a model is already registered, raise AlreadyRegistered.

        If a model is abstract, raise ImproperlyConfigured.
        """
        admin_class = admin_class or ModelAdmin
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if model._meta.abstract:
                raise ImproperlyConfigured(
                    "The model %s is abstract, so it cannot be registered with admin."
                    % model.__name__
                )

            if self.is_registered(model):
                registered_admin = str(self.get_model_admin(model))
                msg = "The model %s is already registered " % model.__name__
                if registered_admin.endswith(".ModelAdmin"):
                    # Most likely registered without a ModelAdmin subclass.
                    msg += "in app %r." % registered_admin.removesuffix(".ModelAdmin")
                else:
                    msg += "with %r." % registered_admin
                raise AlreadyRegistered(msg)

            # Ignore the registration if the model has been
            # swapped out.
            if not model._meta.swapped:
                # If we got **options then dynamically construct a subclass of
                # admin_class with those **options.
                if options:
                    # For reasons I don't quite understand, without a __module__
                    # the created class appears to "live" in the wrong place,
                    # which causes issues later on.
                    options["__module__"] = __name__
                    admin_class = type(
                        "%sAdmin" % model.__name__, (admin_class,), options
                    )

                # Instantiate the admin class to save in the registry
                self._registry[model] = admin_class(model, self)

    def unregister(self, model_or_iterable):
        """
        Unregister the given model(s).

        If a model isn't already registered, raise NotRegistered.
        """
        if isinstance(model_or_iterable, ModelBase):
            model_or_iterable = [model_or_iterable]
        for model in model_or_iterable:
            if not self.is_registered(model):
                raise NotRegistered("The model %s is not registered" % model.__name__)
            del self._registry[model]

    def is_registered(self, model):
        """
        Check if a model class is registered with this `AdminSite`.
        """
        return model in self._registry

    def get_model_admin(self, model):
        try:
            return self._registry[model]
        except KeyError:
            raise NotRegistered(f"The model {model.__name__} is not registered.")

    def add_action(self, action, name=None):
        """
        Register an action to be available globally.
        """
        name = name or action.__name__
        self._actions[name] = action
        self._global_actions[name] = action

    def disable_action(self, name):
        """
        Disable a globally-registered action. Raise KeyError for invalid names.
        """
        del self._actions[name]

    def get_action(self, name):
        """
        Explicitly get a registered global action whether it's enabled or
        not. Raise KeyError for invalid names.
        """
        return self._global_actions[name]

    @property
    def actions(self):
        """
        Get all the enabled actions as an iterable of (name, func).
        """
        return self._actions.items()

    def has_permission(self, request):
        """
        Return True if the given HttpRequest has permission to view
        *at least one* page in the admin site.
        """
        return True

    def admin_view(self, view, cacheable=False):
        """
        Decorator to create an admin view attached to this ``AdminSite``. This
        wraps the view and provides permission checking by calling
        ``self.has_permission``.

        You'll want to use this from within ``AdminSite.get_urls()``:

            class MyAdminSite(AdminSite):

                def get_urls(self):
                    from ginger.urls import path

                    urls = super().get_urls()
                    urls += [
                        path('my_view/', self.admin_view(some_view))
                    ]
                    return urls

        By default, admin_views are marked non-cacheable using the
        ``never_cache`` decorator. If the view can be safely cached, set
        cacheable=True.
        """

        def inner(request, *args, **kwargs):
            return view(request, *args, **kwargs)

        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, "csrf_exempt", False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)

    def get_urls(self):
        # Since this module gets imported in the application's root package,
        # it cannot import models from other applications at the module level,
        from ginger.urls import include, path, re_path

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)

            wrapper.admin_site = self
            return update_wrapper(wrapper, view)

        # Admin-site-wide views.
        urlpatterns = [
            path("", wrap(self.index), name="index"),
            path("autocomplete/", wrap(self.autocomplete_view), name="autocomplete"),
            path("jsi18n/", wrap(self.i18n_javascript, cacheable=True), name="jsi18n"),
        ]

        # Add in each model's views, and create a list of valid URLS for the
        # app_index
        valid_app_labels = []
        for model, model_admin in self._registry.items():
            urlpatterns += [
                path(
                    "%s/%s/" % (model._meta.app_label, model._meta.model_name),
                    include(model_admin.urls),
                ),
            ]
            if model._meta.app_label not in valid_app_labels:
                valid_app_labels.append(model._meta.app_label)

        # If there were ModelAdmins registered, we should have a list of app
        # labels for which we need to allow access to the app_index view,
        if valid_app_labels:
            regex = r"^(?P<app_label>" + "|".join(valid_app_labels) + ")/$"
            urlpatterns += [
                re_path(regex, wrap(self.app_index), name="app_list"),
            ]

        if self.final_catch_all_view:
            urlpatterns.append(re_path(r"(?P<url>.*)$", wrap(self.catch_all_view)))

        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), "admin", self.name

    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        script_name = request.META["SCRIPT_NAME"]
        site_url = (
            script_name if self.site_url == "/" and script_name else self.site_url
        )
        return {
            "site_title": self.site_title,
            "site_header": self.site_header,
            "site_url": site_url,
            "has_permission": self.has_permission(request),
            "available_apps": self.get_app_list(request),
            "is_popup": False,
            "is_nav_sidebar_enabled": self.enable_nav_sidebar,
        }

    def i18n_javascript(self, request, extra_context=None):
        """
        Display the i18n JavaScript that the Ginger admin requires.

        `extra_context` is unused but present for consistency with the other
        admin views.
        """
        return JavaScriptCatalog.as_view(packages=["ginger.contrib.admin"])(request)


    def autocomplete_view(self, request):
        return AutocompleteJsonView.as_view(admin_site=self)(request)

    @no_append_slash
    def catch_all_view(self, request, url):
        if settings.APPEND_SLASH and not url.endswith("/"):
            urlconf = getattr(request, "urlconf", None)
            try:
                match = resolve("%s/" % request.path_info, urlconf)
            except Resolver404:
                pass
            else:
                if getattr(match.func, "should_append_slash", True):
                    return HttpResponsePermanentRedirect(
                        request.get_full_path(force_append_slash=True)
                    )
        raise Http404

    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a
                for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            print(model)
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            # if not has_module_perms:
            #     continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            # if True not in perms.values():
            #     continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                "model": model,
                "name": capfirst(model._meta.verbose_name_plural),
                "object_name": model._meta.object_name,
                "perms": perms,
                "admin_url": None,
                "add_url": None,
            }
            if True:
                model_dict["view_only"] = False
                try:
                    model_dict["admin_url"] = reverse(
                        "admin:%s_%s_changelist" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass
            if True:
                try:
                    model_dict["add_url"] = reverse(
                        "admin:%s_%s_add" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass
            if app_label in app_dict:
                app_dict[app_label]["models"].append(model_dict)
            else:
                app_dict[app_label] = {
                    "name": apps.get_app_config(app_label).verbose_name,
                    "app_label": app_label,
                    "app_url": reverse(
                        "admin:app_list",
                        kwargs={"app_label": app_label},
                        current_app=self.name,
                    ),
                    "has_module_perms": True,
                    "models": [model_dict],
                }
        return app_dict

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])

        return app_list

    def index(self, request, extra_context=None):
        """
        Display the main admin index page, which lists all of the installed
        apps that have been registered in this site.
        """
        app_list = self.get_app_list(request)

        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            "app_list": app_list,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )

    def app_index(self, request, app_label, extra_context=None):
        app_list = self.get_app_list(request, app_label)

        if not app_list:
            raise Http404("The requested admin page does not exist.")

        context = {
            **self.each_context(request),
            "title": _("%(app)s administration") % {"app": app_list[0]["name"]},
            "subtitle": None,
            "app_list": app_list,
            "app_label": app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(
            request,
            self.app_index_template
            or ["admin/%s/app_index.html" % app_label, "admin/app_index.html"],
            context,
        )



class DefaultAdminSite(LazyObject):
    def _setup(self):
        AdminSiteClass = import_string(apps.get_app_config("admin").default_site)
        self._wrapped = AdminSiteClass()

    def __repr__(self):
        return repr(self._wrapped)


# This global object represents the default admin site, for the common case.
# You can provide your own AdminSite using the (Simple)AdminConfig.default_site
# attribute. You can also instantiate AdminSite in your own code to create a
# custom admin site.
site = DefaultAdminSite()
