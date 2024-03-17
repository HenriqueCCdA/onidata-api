from decimal import Decimal

import pytest
from model_bakery import baker

from app.core.models import Loan


@pytest.fixture()
def create_loan_payload():
    return {
        "nominal_value": "1000.00",
        "interest_rate": "40.00",
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
    return baker.make(Loan, user=user_with_token, nominal_value=Decimal("10000.00"), interest_rate=Decimal("10.00"))
