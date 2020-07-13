from django.http import HttpResponse
from django.middleware.csrf import get_token


def csrf(request):
    get_token(request)
    return HttpResponse(status=204)
