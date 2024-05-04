from ginger.shortcuts import render
from ginger.http import JsonResponse
from .models import *
from ginger.rest_framework.decorators import api_view
from ginger.drf_yasg.utils import swagger_auto_schema
from ginger.rest_framework import serializers
from ginger.drf_yasg import openapi

# Create your views here.

def test_view(request):
    print(Tenant.objects.all())
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
    return JsonResponse({"text": "Just rendering some JSON :)"})


