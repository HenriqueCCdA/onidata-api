import pytest
from django.shortcuts import resolve_url
from rest_framework import status

from app.core.models import Payment

URL = resolve_url("core:payments-list-create")


@pytest.mark.integration()
def test_positive(client_api_auth, create_payment_payload):

    response = client_api_auth.post(URL, data=create_payment_payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED

    body = response.json()

    payment_from_db = Payment.objects.first()

    assert body["value"] == str(payment_from_db.value)
    assert body["loan"] == str(payment_from_db.loan.uuid)
    assert body["created_at"] == payment_from_db.created_at.astimezone().isoformat()
    assert body["modified_at"] == payment_from_db.modified_at.astimezone().isoformat()


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
            "loan",
            "1",
            "Must be a valid UUID.",
        ),
        (
            "loan",
            "10ad5e50-0068-4898-a84e-2b0ffb3333ae",
            'Pk inválido "10ad5e50-0068-4898-a84e-2b0ffb3333ae" - objeto não existe.',
        ),
    ],
    ids=[
        "value_lt_zero",
        "value_NaN",
        "loan_invalid_id",
        "loan_id_not_exists",
    ],
)
def test_negative_invalid_value(client_api_auth, create_payment_payload, field, value, error):

    create_payment_payload[field] = value

    response = client_api_auth.post(URL, data=create_payment_payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()

    assert body[field] == [error]


@pytest.mark.integration()
@pytest.mark.parametrize(
    "field",
    [
        "value",
        "loan",
    ],
)
def test_negative_missing_fields(client_api_auth, create_payment_payload, field):

    data = create_payment_payload.copy()
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
