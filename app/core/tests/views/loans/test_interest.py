from uuid import uuid4

import pytest
from django.shortcuts import resolve_url
from rest_framework import status

END_POINT_NAME = "core:loan-with-interest"


@pytest.mark.integration()
def test_positive(client_api_auth, loan_10000_with_10_interest_rate):

    url = resolve_url(END_POINT_NAME, loan_10000_with_10_interest_rate.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["total"] == "14000.00"
    assert body["interest"] == "4000.00"


@pytest.mark.integration()
def test_positive_simple_interest(client_api_auth, loan_10000_with_10_interest_rate):

    url = resolve_url(END_POINT_NAME, loan_10000_with_10_interest_rate.uuid)

    response = client_api_auth.get(f"{url}?interest=simple")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["total"] == "14000.00"
    assert body["interest"] == "4000.00"


@pytest.mark.integration()
def test_positive_compound_interest(client_api_auth, loan_10000_with_10_interest_rate):

    url = resolve_url(END_POINT_NAME, loan_10000_with_10_interest_rate.uuid)

    response = client_api_auth.get(f"{url}?interest=compound")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert body["total"] == "14641.00"
    assert body["interest"] == "4641.00"


@pytest.mark.integration()
def test_negative_user_cannot_see_another_user_loan(client_api_auth, other_user_loan):

    url = resolve_url(END_POINT_NAME, other_user_loan.uuid)

    response = client_api_auth.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()

    assert body == {"detail": "Não encontrado."}


@pytest.mark.integration()
def test_negative_not_found(client_api_auth):

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
