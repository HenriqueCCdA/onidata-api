from datetime import timedelta
from decimal import Decimal

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

    assert body["uuid"] == str(payment_from_db.uuid)
    assert body["value"] == str(payment_from_db.value)
    assert body["loan"] == str(payment_from_db.loan.uuid)
    assert body["payment_date"] == payment_from_db.payment_date.isoformat()
    assert body["created_at"] == payment_from_db.created_at.astimezone().isoformat()
    assert body["modified_at"] == payment_from_db.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_negative_payment_cannot_exceed_the_total_debt(client_api_auth, loan_with_payments):

    data = {
        "value": loan_with_payments.amount_due + Decimal("0.01"),
        "loan": str(loan_with_payments.uuid),
        "payment_date": loan_with_payments.request_date + timedelta(days=60),
    }

    response = client_api_auth.post(URL, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()

    assert body["value"] == ['O pagamento "12500.01" é maior que divida "12500.00" atual.']


@pytest.mark.integration()
def test_negative_payment_cannot_be_made_before_the_loan_request(client_api_auth, payment_in_the_past):

    response = client_api_auth.post(URL, data=payment_in_the_past, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()

    msg = 'O data do pagamento "2024-01-01" é antes da data de requisição "2024-01-02" do emprestimo.'
    assert body["payment_date"] == [msg]


@pytest.mark.integration()
def test_negative_user_not_must_pay_other_user_loan(client_api_auth, create_payment_payload, other_user_loan):

    data = create_payment_payload.copy()

    data["loan"] = other_user_loan.uuid

    response = client_api_auth.post(URL, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    assert not Payment.objects.exists()

    body = response.json()

    assert body == {"loan": [f'Pk inválido "{other_user_loan.uuid}" - objeto não existe.']}


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
        (
            "payment_date",
            "not_a_valid_date",
            "Formato inválido para data. Use um dos formatos a seguir: YYYY-MM-DD.",
        ),
    ],
    ids=[
        "value_lt_zero",
        "value_NaN",
        "loan_invalid_id",
        "loan_id_not_exists",
        "payment_date_not_a_valid_date",
    ],
)
def test_negative_invalid_value(client_api_auth, create_payment_payload, field, value, error):

    create_payment_payload[field] = value

    response = client_api_auth.post(URL, data=create_payment_payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    body = response.json()

    assert body[field] == [error]


@pytest.mark.integration()
@pytest.mark.parametrize("field", ["value", "loan"])
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
