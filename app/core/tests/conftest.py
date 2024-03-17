from decimal import Decimal

import pytest
from model_bakery import baker

from app.core.models import Loan


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
