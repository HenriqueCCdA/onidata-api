from datetime import datetime

import pytest
from model_bakery import baker

from app.core.models import Payment


@pytest.mark.unity()
def test_model_fiels():
    assert Payment._meta.get_field("loan")
    assert Payment._meta.get_field("value")
    assert Payment._meta.get_field("created_at")
    assert Payment._meta.get_field("modified_at")


@pytest.mark.unity()
def test_model_metadata_payment_value():

    value = Payment._meta.get_field("value")
    assert value.max_digits == 14
    assert value.decimal_places == 2


@pytest.mark.integration()
def test_create_at_and_modified_at(payment):
    assert isinstance(payment.created_at, datetime)
    assert isinstance(payment.modified_at, datetime)


@pytest.mark.integration()
def test_str(payment):
    assert str(payment) == f"(id={payment.id},loan_id={payment.loan.id},value={payment.value})"


@pytest.mark.integration()
def test_relationship(loan):

    payment1, payment2 = baker.make(Payment, loan=loan, _quantity=2)

    assert loan.payments.count() == 2
    assert payment1.loan == loan
    assert payment2.loan == loan
