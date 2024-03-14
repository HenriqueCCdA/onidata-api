from django.urls import path

from .views import api_version, get_client_ip

urlpatterns = [
    path("version", api_version, name="api_version"),
    path("get_client_ip", get_client_ip, name="get_client_ip"),
]
