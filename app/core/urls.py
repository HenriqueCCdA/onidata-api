from django.urls import path

from .views import get_client_ip, loans_lc, payment_lc

app_name = "core"
urlpatterns = [
    path("get_client_ip", get_client_ip, name="get-client-ip"),
    path("loans", loans_lc, name="loans-list-create"),
    path("payments", payment_lc, name="payments-list-create"),
]
