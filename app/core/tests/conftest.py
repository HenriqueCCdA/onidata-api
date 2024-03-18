from decimal import Decimal

import pytest
from model_bakery import baker

from app.core.models import Loan, Payment


@pytest.fixture()
def loan(user_with_token):
    return baker.make(Loan, user=user_with_token)


@pytest.fixture()
def other_user_loan(other_user):
    return baker.make(Loan, user=other_user)


@pytest.fixture()
def two_loans(user_with_token):
    return baker.make(Loan, user=user_with_token, _quantity=2)


@pytest.fixture()
def payment(loan):
    return baker.make(Payment, loan=loan)


@pytest.fixture()
def other_user_payment(other_user_loan):
    return baker.make(Payment, loan=other_user_loan)


@pytest.fixture()
def two_payments(loan):
    return baker.make(Payment, loan=loan, _quantity=2)


@pytest.fixture()
def loans_of_two_users(user_with_token, other_user):
    return {
        "user_with_token": baker.make(Loan, user=user_with_token, _quantity=2),
        "other_user": baker.make(Loan, user=other_user, _quantity=3),
    }


@pytest.fixture()
def payments_of_two_users(user_with_token, other_user):

    loan = baker.make(Loan, user=user_with_token)
    loan_other_user = baker.make(Loan, user=other_user)

    return {
        "user_with_token": baker.make(Payment, loan=loan, _quantity=3),
        "other_user": baker.make(Payment, loan=loan_other_user, _quantity=2),
    }


@pytest.fixture()
def create_loan_payload():
    return {
        "value": "1000.00",
        "rate": "40.00",
        "contracted_period": 12,
        "bank": "Banco do Brasil",
    }


@pytest.fixture()
def create_payment_payload(loan):
    return {
        "value": "1000.00",
        "loan": str(loan.uuid),
    }


@pytest.fixture()
def loan_10000_with_10_interest_rate(user_with_token):
    return baker.make(
        Loan,
        user=user_with_token,
        value=Decimal("10000.00"),
        rate=Decimal("10.00"),
        contracted_period=4,
    )


@pytest.fixture()
def loan_with_payments(loan_10000_with_10_interest_rate):

    Payment.objects.bulk_create(
        [
            Payment(loan=loan_10000_with_10_interest_rate, value=200.49),
            Payment(loan=loan_10000_with_10_interest_rate, value=299.51),
            Payment(loan=loan_10000_with_10_interest_rate, value=1000.00),
        ]
    )

    return loan_10000_with_10_interest_rate
