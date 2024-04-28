from ginger.urls import path


def some_view(request):
    pass


urlpatterns = [
    path("some-url/", some_view, name="some-view"),
]
