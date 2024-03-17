from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from django.test import RequestFactory

from app.conftest import fake
from app.core.models import Payment
from app.core.services import extract_client_id, loan_with_interest, total_payment_for_the_loan


@pytest.mark.unity()
@pytest.mark.parametrize("ip", [fake.ipv4(), fake.ipv6()])
def test_positive_extract_client_id_without_x_forwared_for(ip):

    request = RequestFactory().get("/", REMOTE_ADDR=ip)

    assert extract_client_id(request.META) == ip


@pytest.mark.unity()
@pytest.mark.parametrize("ips", [f"{fake.ipv4(), fake.ipv4()}", f"{fake.ipv6(), fake.ipv6()}"], ids=["ipv4", "ipv6"])
def test_positive_extract_client_id_with_x_forwared_for(ips):

    request = RequestFactory().get("/", headers={"X_FORWARDED_FOR": ips})

    expected_client_ip = ips.split(",")[0]

    assert extract_client_id(request.META) == expected_client_ip


@pytest.mark.integration()
def test_positive_loan_payments_sum(loan):

    Payment.objects.bulk_create(
        [
            Payment(loan=loan, value=200.49),
            Payment(loan=loan, value=299.51),
            Payment(loan=loan, value=1000.00),
        ]
    )

    total = total_payment_for_the_loan(loan)

    assert total == Decimal(1500.00)


@pytest.mark.integration()
def test_negative_loan_payments_sum_without_any_payments(loan):

    total = total_payment_for_the_loan(loan)

    assert total == Decimal(0.00)


@pytest.mark.unity()
@pytest.mark.parametrize(
    ("days", "total", "interest", "compound_interest"),
    [
        (30, Decimal("11000.00"), Decimal("1000.00"), False),
        (45, Decimal("11500.00"), Decimal("1500.00"), False),
        (60, Decimal("12000.00"), Decimal("2000.00"), False),
        (30, Decimal("11000.00"), Decimal("1000.00"), True),
        (45, Decimal("11536.90"), Decimal("1536.90"), True),
        (60, Decimal("12100.00"), Decimal("2100.00"), True),
    ],
    ids=[
        "days=30, simple",
        "days=45, simple",
        "days=60, simple",
        "days=30, compound",
        "days=45, compound",
        "days=60, compound",
    ],
)
def test_positive_loan_with_interest(days, total, interest, compound_interest, loan_10000_with_10_interest_rate):

    principal = loan_10000_with_10_interest_rate.nominal_value
    interest_rate = loan_10000_with_10_interest_rate.interest_rate
    initial_date = datetime(2024, 1, 1)
    current_date = timedelta(days=days) + initial_date

    result = loan_with_interest(principal, interest_rate, initial_date, current_date, compound_interest)

    assert result.total == total
    assert result.interest == interest
