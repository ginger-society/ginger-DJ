from ginger.http import HttpResponse


def secure_view(request):
    return HttpResponse(str(request.POST))


def secure_view2(request):
    return HttpResponse(str(request.POST))
