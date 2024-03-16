import pytest
from django.shortcuts import resolve_url
from rest_framework import status

URL = resolve_url("core:payments-list-create")


@pytest.mark.integration()
def test_positive(client_api_auth, payments_of_two_users):

    response = client_api_auth.get(URL)

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    payments_of_user_with_token = payments_of_two_users["user_with_token"]

    assert len(body) == 3

    for b, e in zip(body, payments_of_user_with_token):
        assert b["value"] == str(e.value)
        assert b["loan"] == str(e.loan.uuid)
        assert b["created_at"] == e.created_at.astimezone().isoformat()
        assert b["modified_at"] == e.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_negative_wrong_token(client_api, db):

    client_api.credentials(HTTP_AUTHORIZATION="Token invalid_token")

    response = client_api.get(URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "Token inválido."}


@pytest.mark.integration()
def test_negative_without_token(client_api):

    response = client_api.get(URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "As credenciais de autenticação não foram fornecidas."}
