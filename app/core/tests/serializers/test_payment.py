from decimal import Decimal

import pytest
from django.test import RequestFactory

from app.conftest import fake
from app.core.models import Payment
from app.core.serializers import PaymentSerializer


@pytest.mark.integration()
def test_positive_serialization_objs_list(two_payments):
    request = RequestFactory().request()

    serializer = PaymentSerializer(instance=Payment.objects.all(), many=True, context={"request": request})
    for data, db in zip(serializer.data, two_payments):
        assert data["uuid"] == str(db.uuid)
        assert data["loan"] == str(db.loan.uuid)
        assert data["value"] == str(db.value)
        assert data["payment_date"] == db.payment_date.isoformat()
        assert data["created_at"] == db.created_at.astimezone().isoformat()
        assert data["modified_at"] == db.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_positive_serialization_one_obj(payment):
    request = RequestFactory().request()

    serializer = PaymentSerializer(instance=payment, context={"request": request})

    data = serializer.data

    assert data["uuid"] == str(payment.uuid)
    assert data["loan"] == str(payment.loan.uuid)
    assert data["value"] == str(payment.value)
    assert data["payment_date"] == payment.payment_date.isoformat()
    assert data["created_at"] == payment.created_at.astimezone().isoformat()
    assert data["modified_at"] == payment.modified_at.astimezone().isoformat()


@pytest.mark.unity()
@pytest.mark.parametrize(
    "field",
    [
        "value",
        "loan",
        "payment_date",
    ],
)
def test_negative_missing_fields(field, create_payment_payload):
    data = create_payment_payload.copy()

    del data[field]

    serializer = PaymentSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == ["Este campo é obrigatório."]


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
def test_negative_validation_errors(field, value, error, create_payment_payload, user_with_token):

    data = create_payment_payload.copy()

    request = RequestFactory().request()

    request.user = user_with_token

    data[field] = value

    serializer = PaymentSerializer(data=data, context={"request": request})

    assert not serializer.is_valid()

    assert serializer.errors[field] == [error]


@pytest.mark.integration()
def test_negative_payment_cannot_be_made_before_the_loan_request(payment_in_the_past, user_with_token):

    request = RequestFactory().request()
    request.user = user_with_token

    serializer = PaymentSerializer(data=payment_in_the_past, context={"request": request})

    assert not serializer.is_valid()

    expected_msg = 'O data do pagamento "2024-01-01" é antes da data de requisição "2024-01-02" do emprestimo.'

    assert serializer.errors["payment_date"] == [expected_msg]


@pytest.mark.integration()
def test_positive_create(create_payment_payload, user_with_token):

    request = RequestFactory().request()

    request.user = user_with_token

    serializer = PaymentSerializer(data=create_payment_payload, context={"request": request})

    assert serializer.is_valid()

    serializer.save()

    assert Payment.objects.exists()


@pytest.mark.integration()
def test_negative_create_payment_cannot_exceed_the_total_debt(loan_with_payments):

    request = RequestFactory().request()

    request.user = loan_with_payments.user

    data = {
        "value": loan_with_payments.amount_due + Decimal("10.00"),
        "loan": str(loan_with_payments.uuid),
        "payment_date": fake.date(),
    }

    serializer = PaymentSerializer(data=data, context={"request": request})

    assert not serializer.is_valid()

    assert serializer.errors == {"value": ['O pagamento "12510.00" é maior que divida "12500.00" atual.']}
