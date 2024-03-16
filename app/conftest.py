import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from app.core.models import Loan, Payment

User = get_user_model()

fake = Faker()


@pytest.fixture()
def user(db):
    return baker.make(User)


@pytest.fixture()
def other_user(user):
    return baker.make(User)


@pytest.fixture()
def user_with_password(db):
    password = fake.password()
    user = User.objects.create(email=fake.email(), password=password)
    user.plain_password = password
    return user


@pytest.fixture()
def user_with_token(user_with_password):
    Token.objects.create(user=user_with_password)
    return user_with_password


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
def client_api():
    return APIClient()


@pytest.fixture()
def client_api_auth(client_api, user_with_token):
    client_api.credentials(HTTP_AUTHORIZATION="Token " + user_with_token.auth_token.key)
    return client_api
