from ginger.shortcuts import render
from ginger.http import JsonResponse
from .models import *
from ginger.rest_framework.decorators import api_view
# Create your views here.

def test_view(request):
    print(Tenant.objects.all())
    return JsonResponse({"ok": "yes"})


@api_view(["GET"])
def test_view2(request):
    """Test view"""
    return JsonResponse({"text": "Just rendering some JSON :)"})