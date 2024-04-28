from ginger.shortcuts import render
from ginger.http import JsonResponse
from .models import *
# Create your views here.

def test_view(request):
    print(Tenant.objects.all())
    return JsonResponse({"ok": "yes"})