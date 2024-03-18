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

    # TODO: Testar o retorn com payload
    assert body["uuid"] == str(loan_from_db.uuid)
    assert body["value"] == str(loan_from_db.value)
    assert body["rate"] == str(loan_from_db.rate)
    assert body["contracted_period"] == loan_from_db.contracted_period
    assert body["register_ip"] == loan_from_db.register_ip
    assert body["bank"] == loan_from_db.bank
    assert body["request_date"] == loan_from_db.request_date.isoformat()
    assert body["created_at"] == loan_from_db.created_at.astimezone().isoformat()
    assert body["modified_at"] == loan_from_db.modified_at.astimezone().isoformat()


@pytest.mark.integration()
@pytest.mark.parametrize(
    ("field", "value", "error"),
    [
        (
            "value",
            "-1.0",
            "Certifque-se de que este valor seja maior ou igual a 0.0.",
        ),
        (
            "value",
            "NaN",
            "Um número válido é necessário.",
        ),
        (
            "rate",
            "-1.0",
            "Certifque-se de que este valor seja maior ou igual a 0.0.",
        ),
        (
            "rate",
            "NaN",
            "Um número válido é necessário.",
        ),
        (
            "bank",
            101 * "F",
            "Certifique-se de que este campo não tenha mais de 100 caracteres.",
        ),
        (
            "contracted_period",
            "-1",
            "Certifque-se de que este valor seja maior ou igual a 0.",
        ),
        (
            "contracted_period",
            "NaN",
            "Um número inteiro válido é exigido.",
        ),
        (
            "request_date",
            "not_a_valid_date",
            "Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.",
        ),
    ],
    ids=[
        "nominal_value_lt_zero",
        "nominal_value_NaN",
        "interest_rate_lt_zero",
        "interest_rate_NaN",
        "bank_lenght_gt_100",
        "contracted_period_lt_zero",
        "contracted_period_NaN",
        "request_date_not_a_valid_date",
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
        "value",
        "rate",
        "bank",
        "contracted_period",
        "request_date",
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
