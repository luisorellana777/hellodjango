from django.urls import path

from . import views

urlpatterns = [
    path("hello", views.HelloView.as_view()),
    path("api/ping", views.PingView.as_view()),
    path("api/hello-phone", views.HelloPhoneView.as_view()),
]

