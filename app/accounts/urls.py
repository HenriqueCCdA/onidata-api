from django.urls import path

from .views import obtain_auth_token, whoiam

urlpatterns = [
    path("auth/token", obtain_auth_token, name="get_token"),
    path("auth/whoiam", whoiam, name="whoiam"),
]
