from django.urls import path

from .views import api_version

urlpatterns = [
    path("version", api_version, name="api_version"),
]
