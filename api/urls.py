from django.urls import path

from . import views

urlpatterns = [
    path("hello", views.hello),
    path("api/ping", views.ping),
    path("api/hello-phone", views.hello_phone),
]

