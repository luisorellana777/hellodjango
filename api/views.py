import json
from dataclasses import dataclass

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods


@require_GET
def hello(request):
    return HttpResponse("Hello, world")


@require_GET
def ping(request):
    return JsonResponse({"status": "ok"})


@dataclass
class PersonInfo:
    name: str
    phone_number: str

    @classmethod
    def from_payload(cls, payload: dict) -> "PersonInfo":
        name = payload.get("name")
        phone_number = payload.get("phone_number")

        if not name or not phone_number:
            raise ValueError("Missing required fields: name, phone_number")

        return cls(name=name, phone_number=phone_number)


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
