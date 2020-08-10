from mimetypes import guess_type

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.middleware.csrf import get_token

from backend.model.TutorialRelatedModel import Uploads


def csrf(request: HttpRequest) -> JsonResponse:
    return JsonResponse({'csrfToken': get_token(request)})


def media_request(request: HttpRequest, url: str) -> HttpResponse:
    if request.method == 'GET':
        try:
            upload = Uploads.objects.get(file=url)
            file = upload.file
            return HttpResponse(content=file, content_type=guess_type(file.path)[0])
        except Uploads.DoesNotExist:
            return HttpResponse(status=404)
    return HttpResponse(status=400)
