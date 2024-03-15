import pytest


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
