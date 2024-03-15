import pytest
from django.shortcuts import resolve_url
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

URL = resolve_url("accounts:whoiam")


@pytest.mark.integration()
def test_positive(client_api_auth, user_with_token):

    response = client_api_auth.get(URL)

    assert response.status_code == HTTP_200_OK

    body = response.json()

    assert body["id"] == user_with_token.pk
    assert body["email"] == user_with_token.email
    assert body["created_at"] == user_with_token.created_at.astimezone().isoformat()
    assert body["modified_at"] == user_with_token.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_negative_invalid_token(client_api, user_with_token):

    client_api.credentials(HTTP_AUTHORIZATION="Token " + user_with_token.auth_token.key + "1")

    response = client_api.get(URL)

    assert response.status_code == HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "Token inválido."}


@pytest.mark.integration()
def test_negative_without_token(client):

    response = client.get(URL)

    assert response.status_code == HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "As credenciais de autenticação não foram fornecidas."}

    assert response.headers["WWW-Authenticate"] == "Token"
