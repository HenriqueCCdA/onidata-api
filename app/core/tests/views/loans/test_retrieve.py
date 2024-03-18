from uuid import uuid4

import pytest
from django.shortcuts import resolve_url
from rest_framework import status

END_POINT_NAME = "core:loan-retrieve"


@pytest.mark.integration()
def test_positive(client_api_auth, loan):

    url = resolve_url(END_POINT_NAME, loan.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["uuid"] == str(loan.uuid)
    assert body["value"] == str(loan.value)
    assert body["rate"] == str(loan.rate)
    assert body["contracted_period"] == loan.contracted_period
    assert body["register_ip"] == loan.register_ip
    assert body["payments"] == [p["id"] for p in loan.payments.values("id")]
    assert body["bank"] == loan.bank
    assert body["request_date"] == loan.request_date.isoformat()
    assert body["created_at"] == loan.created_at.astimezone().isoformat()
    assert body["modified_at"] == loan.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_negative_user_not_must_retrieve_other_user_loan(client_api_auth, other_user_loan):

    url = resolve_url(END_POINT_NAME, other_user_loan.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert response.json() == {"detail": "Você não tem permissão para executar essa ação."}


@pytest.mark.integration()
def test_negative_wrong_token(client_api, db):

    url = resolve_url(END_POINT_NAME, uuid4())

    client_api.credentials(HTTP_AUTHORIZATION="Token invalid_token")

    response = client_api.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    assert response.json() == {"detail": "Token inválido."}


@pytest.mark.integration()
def test_negative_without_token(client_api):

    url = resolve_url(END_POINT_NAME, uuid4())

    response = client_api.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    assert response.json() == {"detail": "As credenciais de autenticação não foram fornecidas."}
