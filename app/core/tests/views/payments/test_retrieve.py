from uuid import uuid4

import pytest
from django.shortcuts import resolve_url
from rest_framework import status

END_POINT_NAME = "core:payment-retrieve"


@pytest.mark.integration()
def test_positive(client_api_auth, payment):

    url = resolve_url(END_POINT_NAME, payment.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["uuid"] == str(payment.uuid)
    assert body["value"] == str(payment.value)
    assert body["loan"] == str(payment.loan.uuid)
    assert body["created_at"] == payment.created_at.astimezone().isoformat()
    assert body["modified_at"] == payment.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_negative_user_not_must_retrieve_other_user_payment(client_api_auth, other_user_payment):

    url = resolve_url(END_POINT_NAME, other_user_payment.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    assert response.json() == {"detail": "Você não tem permissão para executar essa ação."}


@pytest.mark.integration()
def test_negative_wrong_token(client_api, db):

    url = resolve_url(END_POINT_NAME, uuid4())

    client_api.credentials(HTTP_AUTHORIZATION="Token invalid_token")

    response = client_api.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "Token inválido."}


@pytest.mark.integration()
def test_negative_without_token(client_api):

    url = resolve_url(END_POINT_NAME, uuid4())

    response = client_api.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "As credenciais de autenticação não foram fornecidas."}
