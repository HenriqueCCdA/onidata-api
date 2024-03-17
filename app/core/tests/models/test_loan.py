from datetime import datetime

import pytest

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
