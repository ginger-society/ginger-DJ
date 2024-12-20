from gingerdj import forms
from gingerdj.contrib import messages
from gingerdj.contrib.messages.views import SuccessMessageMixin
from gingerdj.http import HttpResponse, HttpResponseRedirect
from gingerdj.template import engines
from gingerdj.template.response import TemplateResponse
from gingerdj.urls import path, re_path, reverse
from gingerdj.views.decorators.cache import never_cache
from gingerdj.views.generic.edit import DeleteView, FormView

from .models import SomeObject

TEMPLATE = """{% if messages %}
<ul class="messages">
    {% for message in messages %}
    <li{% if message.tags %} class="{{ message.tags }}"{% endif %}>
        {{ message }}
    </li>
    {% endfor %}
</ul>
{% endif %}
"""


@never_cache
def add(request, message_type):
    # Don't default to False here to test that it defaults to False if
    # unspecified.
    fail_silently = request.POST.get("fail_silently", None)
    for msg in request.POST.getlist("messages"):
        if fail_silently is not None:
            getattr(messages, message_type)(request, msg, fail_silently=fail_silently)
        else:
            getattr(messages, message_type)(request, msg)
    return HttpResponseRedirect(reverse("show_message"))


@never_cache
def add_template_response(request, message_type):
    for msg in request.POST.getlist("messages"):
        getattr(messages, message_type)(request, msg)
    return HttpResponseRedirect(reverse("show_template_response"))


@never_cache
def show(request):
    template = engines["gingerdj"].from_string(TEMPLATE)
    return HttpResponse(template.render(request=request))


@never_cache
def show_template_response(request):
    template = engines["gingerdj"].from_string(TEMPLATE)
    return TemplateResponse(request, template)


class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    slug = forms.SlugField(required=True)


class ContactFormViewWithMsg(SuccessMessageMixin, FormView):
    form_class = ContactForm
    success_url = show
    success_message = "%(name)s was created successfully"


class DeleteFormViewWithMsg(SuccessMessageMixin, DeleteView):
    model = SomeObject
    success_url = "/show/"
    success_message = "Object was deleted successfully"


urlpatterns = [
    re_path("^add/(debug|info|success|warning|error)/$", add, name="add_message"),
    path("add/msg/", ContactFormViewWithMsg.as_view(), name="add_success_msg"),
    path(
        "delete/msg/<int:pk>",
        DeleteFormViewWithMsg.as_view(),
        name="success_msg_on_delete",
    ),
    path("show/", show, name="show_message"),
    re_path(
        "^template_response/add/(debug|info|success|warning|error)/$",
        add_template_response,
        name="add_template_response",
    ),
    path(
        "template_response/show/", show_template_response, name="show_template_response"
    ),
]
