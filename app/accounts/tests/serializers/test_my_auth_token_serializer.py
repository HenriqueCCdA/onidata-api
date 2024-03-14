import pytest
from django.contrib.auth import get_user_model
from faker import Faker

from app.accounts.serializers import MyAuthTokenSerializer

fake = Faker()

User = get_user_model()


@pytest.mark.integration
def test_positive_valid_user(payload_get_token):

    serializer = MyAuthTokenSerializer(data=payload_get_token)

    assert serializer.is_valid()

    user = User.objects.get(email=payload_get_token["email"])

    assert serializer.validated_data["user"] == user


@pytest.mark.unity
@pytest.mark.parametrize("field", ["email", "password"])
def test_negative_missing_fields(field):

    data = {
        "email": fake.email(),
        "password": fake.password(),
    }

    del data[field]

    serializer = MyAuthTokenSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == ["Este campo é obrigatório."]


@pytest.mark.integration
def test_negative_wrong_credentials(payload_get_token):

    payload_get_token["password"] = "wrong_password"

    serializer = MyAuthTokenSerializer(data=payload_get_token)

    assert not serializer.is_valid()

    assert serializer.errors["non_field_errors"] == ["Não é possível fazer login com as credenciais fornecidas."]
