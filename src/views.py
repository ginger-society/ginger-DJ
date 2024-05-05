from ginger.shortcuts import render
from ginger.http import JsonResponse
from .models import *
from ginger.rest_framework.decorators import api_view
from ginger.drf_yasg.utils import swagger_auto_schema
from ginger.rest_framework import serializers
from ginger.drf_yasg import openapi
from prometheus_client import Counter

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
    requests_total.labels(endpoint="Health check", method=test_view2, user=None).inc()
    return JsonResponse({"text": "Just rendering some JSON :)"})


