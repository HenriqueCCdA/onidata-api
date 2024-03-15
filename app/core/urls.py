from django.urls import path

from .views import api_version, get_client_ip, loans_lc

app_name = "core"
urlpatterns = [
    path("version", api_version, name="api-version"),
    path("get_client_ip", get_client_ip, name="get-client-ip"),
    path("loans", loans_lc, name="loans-list-create"),
]
