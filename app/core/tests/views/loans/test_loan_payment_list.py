from uuid import uuid4

import pytest
from django.shortcuts import resolve_url
from model_bakery import baker
from rest_framework import status

from app.core.models import Loan

END_POINT_NAME = "core:loan-payment-list"


@pytest.mark.integration()
def test_positive(client_api_auth, loan, two_payments):

    url = resolve_url(END_POINT_NAME, loan.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    payments_of_loan = two_payments

    assert len(body) == 2

    for b, e in zip(body, payments_of_loan):
        assert b["loan"] == str(e.loan.uuid)
        assert b["value"] == str(e.value)
        assert b["created_at"] == e.created_at.astimezone().isoformat()
        assert b["modified_at"] == e.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_negative_user_not_must_list_loan_of_other_user(client_api_auth, loan, other_user):

    loan = baker.make(Loan, user=other_user)

    url = resolve_url(END_POINT_NAME, loan.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()

    assert body == {"detail": "Não encontrado."}


@pytest.mark.integration()
def test_negative_not_found(client_api_auth, loan):

    url = resolve_url(END_POINT_NAME, uuid4())

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()

    assert body == {"detail": "Não encontrado."}


@pytest.mark.integration()
def test_negative_wrong_token(client_api, db):

    url = resolve_url(END_POINT_NAME, uuid4())

    client_api.credentials(HTTP_AUTHORIZATION="Token invalid_token")

    response = client_api.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "Token inválido."}


@pytest.mark.integration()
def test_negative_without_token(client_api, db):

    url = resolve_url(END_POINT_NAME, uuid4())

    response = client_api.get(url)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "As credenciais de autenticação não foram fornecidas."}
