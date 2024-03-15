from django.urls import path

from .views import obtain_auth_token, whoiam

app_name = "accounts"
urlpatterns = [
    path("auth/token", obtain_auth_token, name="get-token"),
    path("auth/whoiam", whoiam, name="whoiam"),
]
