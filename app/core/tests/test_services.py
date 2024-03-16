from decimal import Decimal
from uuid import uuid4

import pytest
from django.test import RequestFactory

from app.conftest import fake
from app.core.models import Payment
from app.core.services import TotalPaymentLoanNotFound, extract_client_id, total_payment_for_the_loan


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

    total = total_payment_for_the_loan(loan.uuid)

    assert total == Decimal(1500.00)


@pytest.mark.integration()
def test_negative_loan_payments_sum_without_any_payments(loan):

    total = total_payment_for_the_loan(loan.uuid)

    assert total == Decimal(0.00)


@pytest.mark.integration()
def test_negative_loan_payments_sum_loan_not_exists(db):

    uuid = uuid4()
    msg = f'Emprestimo com o "{uuid}" não existe.'

    with pytest.raises(TotalPaymentLoanNotFound, match=msg):
        total_payment_for_the_loan(uuid)
