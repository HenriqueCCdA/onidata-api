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
    ("months", "total", "interest", "compound_interest"),
    [
        (6, Decimal("16000.00"), Decimal("6000.00"), False),
        (12, Decimal("22000.00"), Decimal("12000.00"), False),
        (24, Decimal("34000.00"), Decimal("24000.00"), False),
        (6, Decimal("17715.61"), Decimal("7715.61"), True),
        (12, Decimal("31384.28"), Decimal("21384.28"), True),
        (24, Decimal("98497.33"), Decimal("88497.33"), True),
    ],
    ids=[
        "months=6, simple",
        "months=12, simple",
        "months=24, compound",
        "months=6, compound",
        "months=12, compound",
        "months=24, compound",
    ],
)
def test_positive_loan_with_interest(months, total, interest, compound_interest, loan_10000_with_10_interest_rate):

    principal = loan_10000_with_10_interest_rate.value
    rate = loan_10000_with_10_interest_rate.rate

    result = loan_with_interest(principal, rate, months, compound_interest)

    assert result.total == total
    assert result.interest == interest
