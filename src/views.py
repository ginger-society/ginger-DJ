from ginger.shortcuts import render
from ginger.http import JsonResponse
from .models import *
from ginger.rest_framework.decorators import api_view
from ginger.drf_yasg.utils import swagger_auto_schema
from ginger.rest_framework import serializers
from ginger.drf_yasg import openapi
from prometheus_client import Counter
from ginger.views.decorators.cache import cache_page
from datetime import datetime

# Create your views here.

requests_total = Counter(
    name="health_check_total_3",
    documentation="Total number of various requests. - health check",
    labelnames=["endpoint", "method", "user"],
)


def test_view(request):
    return JsonResponse({"ok": "yes"})

class TestReponseSerializer(serializers.Serializer):
    """test model"""

    text = serializers.CharField()

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()


@swagger_auto_schema(method="GET", responses={200: openapi.Response("testResponse", TestReponseSerializer)}, security=[{"Bearer": []}])
@api_view(["GET"])
def test_view2(request):
    """Test view"""
    requests_total.labels(endpoint="Test view 2", method=test_view2, user=None).inc()
    return JsonResponse({"text": "Just rendering some JSON :)"})



@cache_page(10)
def health_check_view(request):
    """Server health check request handler"""
    requests_total.labels(endpoint="Health check", method=health_check_view, user=None).inc()
    now = datetime.now()
    return JsonResponse({"status": "ok", "server_time": now.strftime("%d/%m/%Y, %H:%M:%S")})

