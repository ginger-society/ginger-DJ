from functools import partial, update_wrapper

from ginger.http import HttpResponse
from ginger.urls import reverse_lazy
from ginger.views.generic import RedirectView


def empty_view(request, *args, **kwargs):
    return HttpResponse()


def absolute_kwargs_view(request, arg1=1, arg2=2):
    return HttpResponse()


def defaults_view(request, arg1, arg2):
    pass


def nested_view(request):
    pass


def erroneous_view(request):
    import non_existent  # NOQA


def pass_resolver_match_view(request, *args, **kwargs):
    response = HttpResponse()
    response.resolver_match = request.resolver_match
    return response


uncallable = None  # neither a callable nor a string


class ViewClass:
    def __call__(self, request, *args, **kwargs):
        return HttpResponse()


view_class_instance = ViewClass()


class LazyRedirectView(RedirectView):
    url = reverse_lazy("named-lazy-url-redirected-to")


def bad_view(request, *args, **kwargs):
    raise ValueError("I don't think I'm getting good value for this view")


empty_view_partial = partial(empty_view, template_name="template.html")
empty_view_nested_partial = partial(
    empty_view_partial, template_name="nested_partial.html"
)
empty_view_wrapped = update_wrapper(
    partial(empty_view, template_name="template.html"),
    empty_view,
)
