import pytest
from django.shortcuts import resolve_url
from rest_framework import status

URL = resolve_url("core:loans-list-create")


@pytest.mark.integration()
def test_positive(client_api_auth, loans_of_two_users):

    response = client_api_auth.get(URL)

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    loan_of_user_with_token = loans_of_two_users["user_with_token"]

    assert len(body) == 2

    for b, e in zip(body, loan_of_user_with_token):
        assert b["uuid"] == str(e.uuid)
        assert b["nominal_value"] == str(e.nominal_value)
        assert b["interest_rate"] == str(e.interest_rate)
        assert b["register_ip"] == e.register_ip
        assert b["payments"] == [p["id"] for p in e.payments.values("id")]
        assert b["bank"] == e.bank
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
