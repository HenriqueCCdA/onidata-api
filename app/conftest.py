import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from model_bakery import baker
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

User = get_user_model()

fake = Faker()


@pytest.fixture
def client_api():
    return APIClient()


@pytest.fixture
def user(db):
    return baker.make(User)


@pytest.fixture
def other_user(user):
    return baker.make(User)


@pytest.fixture
def user_with_password(db):
    password = fake.password()
    user = User.objects.create(email=fake.email(), password=password)
    user.plain_password = password
    return user


@pytest.fixture
def user_with_token(user_with_password):
    Token.objects.create(user=user_with_password)
    return user_with_password
