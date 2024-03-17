from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("get_client_ip/", views.get_client_ip, name="get-client-ip"),
    #
    path("loans/", views.loan_lc, name="loans-list-create"),
    path("loans/<uuid:id>/payments/", views.loan_payment_list, name="loan-payment-list"),
    path("loans/<uuid:id>/payments/total/", views.loan_payment_sum, name="loan-payment-sum"),
    path("loans/<uuid:id>/interest/", views.loan_with_interest, name="loan-with-interest"),
    path("loans/<uuid:id>/amount_due/", views.loan_amount_due, name="loan-amount-due"),
    path("loans/<uuid:id>/", views.loan_retrieve, name="loan-retrieve"),
    #
    path("payments/", views.payment_lc, name="payments-list-create"),
    path("payments/<uuid:id>/", views.payment_retrieve, name="payment-retrieve"),
]
