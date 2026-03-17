import json

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from .person import PersonInfo


@require_GET
def hello(request):
    return HttpResponse("Hello, world")


@require_GET
def ping(request):
    return JsonResponse({"status": "ok"})


@csrf_exempt
@require_http_methods(["PUT"])
def hello_phone(request):
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    try:
        person = PersonInfo.from_payload(payload)
    except ValueError as exc:
        return JsonResponse({"error": str(exc)}, status=400)

    return HttpResponse(
        f"Hello {person.name}. Your phone number is {person.phone_number}"
    )
