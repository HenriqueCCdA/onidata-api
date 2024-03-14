import pytest
from django.shortcuts import resolve_url
from faker import Faker
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

fake = Faker()

URL = resolve_url("get_token")


@pytest.mark.integration
def test_positive_with_email_password(client_api, payload_get_token, user_with_password):

    response = client_api.post(URL, data=payload_get_token, format="json")

    assert response.status_code == HTTP_200_OK

    body = response.json()
    token = Token.objects.get(user__id=user_with_password.pk)

    assert body == {"token": token.key}


@pytest.mark.integration
def test_negative_wrong_credentials(client_api, payload_get_token, user_with_password):

    payload_get_token["password"] = "wrong_password"

    response = client_api.post(URL, data=payload_get_token, format="json")

    assert response.status_code == HTTP_400_BAD_REQUEST

    body = response.json()

    assert body["non_field_errors"] == ["Não é possível fazer login com as credenciais fornecidas."]


@pytest.mark.unity
@pytest.mark.parametrize("field", ["email", "password"])
def test_negative_missing_fields(client_api, payload_get_token, field):

    data = payload_get_token.copy()
    del data[field]

    response = client_api.post(URL, data=data, format="json")

    assert response.status_code == HTTP_400_BAD_REQUEST

    body = response.json()

    assert body[field] == ["Este campo é obrigatório."]
