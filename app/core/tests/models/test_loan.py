from datetime import datetime
from decimal import Decimal

import pytest
from model_bakery import baker

from app.core.models import Loan


@pytest.mark.unity()
def test_model_fiels():
    assert Loan._meta.get_field("uuid")
    assert Loan._meta.get_field("value")
    assert Loan._meta.get_field("rate")
    assert Loan._meta.get_field("contracted_period")
    assert Loan._meta.get_field("register_ip")
    assert Loan._meta.get_field("bank")
    assert Loan._meta.get_field("user")
    assert Loan._meta.get_field("created_at")
    assert Loan._meta.get_field("modified_at")


@pytest.mark.unity()
def test_model_metadata_uuid():

    uuid = Loan._meta.get_field("uuid")

    assert not uuid.editable
    assert uuid.unique


@pytest.mark.unity()
def test_model_metadata_nominal_value():

    value = Loan._meta.get_field("value")
    assert value.max_digits == 14
    assert value.decimal_places == 2


@pytest.mark.unity()
def test_model_metadata_interest_rate():

    rate = Loan._meta.get_field("rate")
    assert rate.max_digits == 14
    assert rate.decimal_places == 2


@pytest.mark.unity()
def test_model_metadata_bank():
    bank = Loan._meta.get_field("bank")
    assert bank.max_length == 100


@pytest.mark.unity()
def test_create_at_and_modified_at(loan):
    assert isinstance(loan.created_at, datetime)
    assert isinstance(loan.modified_at, datetime)


@pytest.mark.unity()
def test_str(loan):
    assert str(loan) == str(loan.uuid)


@pytest.mark.integration()
def test_relationship(two_loans, user_with_token):
    assert user_with_token.loans.count() == 2
    assert two_loans[0].user == user_with_token
    assert two_loans[1].user == user_with_token


@pytest.mark.integration()
def test_value_with_interest(loan_10000_with_10_interest_rate):

    assert loan_10000_with_10_interest_rate.value_with_interest.total == Decimal("14000.00")
    assert loan_10000_with_10_interest_rate.value_with_interest.interest == Decimal("4000.00")


@pytest.mark.integration()
def test_value_with_interest_call_once(mocker, db):

    mock = mocker.patch("app.core.models.loan_with_interest")

    loan = baker.make(Loan)

    _ = loan.value_with_interest
    _ = loan.value_with_interest

    assert mock.call_count == 1
