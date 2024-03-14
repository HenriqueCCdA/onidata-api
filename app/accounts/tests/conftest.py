import pytest
from django.contrib.auth import get_user_model
from faker import Faker

User = get_user_model()

fake = Faker()


@pytest.fixture()
def superuser(db):
    return User.objects.create_superuser(email=fake.email(), password=fake.password())


@pytest.fixture()
def payload_get_token(user_with_password):
    return {
        "email": user_with_password.email,
        "password": user_with_password.plain_password,
    }
