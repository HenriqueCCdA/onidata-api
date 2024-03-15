import pytest
from django.test import RequestFactory

from app.core.models import Loan
from app.core.serializers import LoanSerializer


@pytest.mark.integration()
def test_positive_serialization_objs_list(two_loans):
    request = RequestFactory().request()

    serializer = LoanSerializer(instance=Loan.objects.all(), many=True, context={"request": request})

    for data, db in zip(serializer.data, two_loans):
        assert data["uuid"] == str(db.uuid)
        assert data["nominal_value"] == str(db.nominal_value)
        assert data["interest_rate"] == str(db.interest_rate)
        assert data["payments"] == [p["id"] for p in db.payments.values("id")]
        assert data["register_ip"] == db.register_ip
        assert data["bank"] == db.bank
        assert data["created_at"] == db.created_at.astimezone().isoformat()
        assert data["modified_at"] == db.modified_at.astimezone().isoformat()


@pytest.mark.integration()
def test_positive_serialization_one_obj(loan):
    request = RequestFactory().request()

    serializer = LoanSerializer(instance=loan, context={"request": request})

    data = serializer.data

    assert data["uuid"] == str(loan.uuid)
    assert data["nominal_value"] == str(loan.nominal_value)
    assert data["interest_rate"] == str(loan.interest_rate)
    assert data["payments"] == [p["id"] for p in loan.payments.values("id")]
    assert data["register_ip"] == loan.register_ip
    assert data["bank"] == loan.bank
    assert data["created_at"] == loan.created_at.astimezone().isoformat()
    assert data["modified_at"] == loan.modified_at.astimezone().isoformat()


@pytest.mark.integration()
@pytest.mark.parametrize(
    "field",
    [
        "nominal_value",
        "interest_rate",
        "bank",
    ],
)
def test_negative_missing_fields(field, create_loan_payload):
    data = create_loan_payload.copy()

    del data[field]

    serializer = LoanSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == ["Este campo é obrigatório."]


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
def test_negative_validation_errors(field, value, error, create_loan_payload):
    data = create_loan_payload.copy()

    data[field] = value

    serializer = LoanSerializer(data=data)

    assert not serializer.is_valid()

    assert serializer.errors[field] == [error]


@pytest.mark.integration()
def test_positive_create(create_loan_payload, user):

    request = RequestFactory().request()

    request.user = user

    serializer = LoanSerializer(data=create_loan_payload, context={"request": request})

    assert serializer.is_valid()

    serializer.save()

    assert Loan.objects.exists()


@pytest.mark.unity()
def test_negative_create_without_request_in_context(create_loan_payload):
    serializer = LoanSerializer(data=create_loan_payload)

    assert not serializer.is_valid()

    assert serializer.errors["non_field_errors"] == ["O request precisa estar no contexto."]


@pytest.mark.unity()
def test_negative_create_request_without_user(create_loan_payload):

    request = RequestFactory().request()

    serializer = LoanSerializer(data=create_loan_payload, context={"request": request})

    assert not serializer.is_valid()

    assert serializer.errors["non_field_errors"] == ["O user precisa estar no contexto."]
