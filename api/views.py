import json

from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiExample

from .person import PersonInfo


class HelloView(APIView):
    @extend_schema(
        summary="Hello world",
        responses={200: {"type": "string", "example": "Hello, world"}},
        tags=["General"],
    )
    def get(self, request):
        return HttpResponse("Hello, world")


class PingView(APIView):
    @extend_schema(
        summary="Health check",
        responses={200: {"type": "object", "properties": {"status": {"type": "string"}}}},
        tags=["General"],
    )
    def get(self, request):
        return Response({"status": "ok"})


class HelloPhoneView(APIView):
    @extend_schema(
        summary="Greet with phone",
        request={
            "application/json": {
                "type": "object",
                "required": ["name", "phone_number"],
                "properties": {
                    "name": {"type": "string"},
                    "phone_number": {"type": "string"},
                },
            }
        },
        responses={
            200: {"type": "string", "example": "Hello John. Your phone number is +1234567890"},
            400: {"type": "object", "properties": {"error": {"type": "string"}}},
        },
        examples=[
            OpenApiExample(
                "Valid request",
                value={"name": "John", "phone_number": "+1234567890"},
                request_only=True,
            ),
        ],
        tags=["Person"],
    )
    def put(self, request):
        try:
            payload = request.data if request.data else json.loads(
                request.body.decode("utf-8") or "{}"
            )
        except (json.JSONDecodeError, TypeError):
            return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            person = PersonInfo.from_payload(payload)
        except ValueError as exc:
            return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            f"Hello {person.name}. Your phone number is {person.phone_number}"
        )
