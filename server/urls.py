"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.ginger.gloportal.dev/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from ginger.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from ginger.contrib import admin
from ginger.urls import path, include
from src.views import *
from ginger.drf_yasg import openapi
from ginger.drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version="v1.0.0",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    path("swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path('admin/', admin.site.urls),
    path('test/', test_view),
    path('test2/', test_view2),
    path("health-check", health_check_view),
    path("", include("ginger.prometheus.urls")),
]
