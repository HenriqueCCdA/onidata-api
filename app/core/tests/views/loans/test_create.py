import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from app.core.models import Loan

URL = resolve_url("core:loans-list-create")


@pytest.mark.integration()
def test_positive(client_api_auth, create_loan_payload):

    response = client_api_auth.post(URL, data=create_loan_payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    loan_from_db = Loan.objects.first()

    assert body["uuid"] == str(loan_from_db.uuid)
    assert body["nominal_value"] == str(loan_from_db.nominal_value)
    assert body["interest_rate"] == str(loan_from_db.interest_rate)
    assert body["register_ip"] == loan_from_db.register_ip
    assert body["bank"] == loan_from_db.bank
    assert body["created_at"] == loan_from_db.created_at.astimezone().isoformat()
    assert body["modified_at"] == loan_from_db.modified_at.astimezone().isoformat()


@pytest.mark.integration()
@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        (
            "nominal_value",
            "-1.0",
            "Certifque-se de que este valor seja maior ou igual a 0.0.",
        ),
        (
            "nominal_value",
            "NaN",
            "Um número válido é necessário.",
        ),
        (
            "interest_rate",
            "-1.0",
            "Certifque-se de que este valor seja maior ou igual a 0.0.",
        ),
        (
            "interest_rate",
            "NaN",
            "Um número válido é necessário.",
        ),
        (
            "bank",
            101 * "F",
            "Certifique-se de que este campo não tenha mais de 100 caracteres.",
        ),
    ],
    ids=[
        "nominal_value_lt_zero",
        "nominal_value_NaN",
        "interest_rate_lt_zero",
        "interest_rate_NaN",
        "bank_lenght_gt_100",
    ],
)
def test_negative_invalid_value(client_api_auth, create_loan_payload, field, value, error):

    create_loan_payload[field] = value

    response = client_api_auth.post(URL, data=create_loan_payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()

    assert body[field] == [error]


@pytest.mark.integration()
@pytest.mark.parametrize(
    "field",
    [
        "nominal_value",
        "interest_rate",
        "bank",
    ],
)
def test_negative_missing_fields(client_api_auth, create_loan_payload, field):

    data = create_loan_payload.copy()
    del data[field]

    response = client_api_auth.post(URL, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()

    assert body[field] == ["Este campo é obrigatório."]


@pytest.mark.integration()
def test_negative_wrong_token(client_api, db):

    client_api.credentials(HTTP_AUTHORIZATION="Token invalid_token")

    response = client_api.post(URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "Token inválido."}


@pytest.mark.integration()
def test_negative_without_token(client_api):

    response = client_api.post(URL)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    body = response.json()

    assert body == {"detail": "As credenciais de autenticação não foram fornecidas."}
