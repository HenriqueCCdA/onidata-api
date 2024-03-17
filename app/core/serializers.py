from django.forms import ValidationError
from rest_framework import serializers

from app.core.models import Loan, Payment
from app.core.services import extract_client_id


# TODO: Testar
class PaymentSumSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=14, decimal_places=2)


# TODO: Testar
class DebtLoanSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=14, decimal_places=2)
    interest = serializers.DecimalField(max_digits=14, decimal_places=2)


# TODO: Testar
class AmountDueSerializer(serializers.Serializer):
    due = serializers.DecimalField(max_digits=14, decimal_places=2)


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = (
            "uuid",
            "value",
            "rate",
            "contracted_period",
            "register_ip",
            "payments",
            "bank",
            "created_at",
            "modified_at",
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True},
            "register_ip": {"read_only": True},
            "payments": {"read_only": True},
        }

    def create(self, validate_data):

        request = self.context["request"]

        data = {**validate_data, "user": request.user, "register_ip": extract_client_id(request.META)}

        loans = super().create(data)

        return loans

    def validate(self, attrs):

        try:
            request = self.context["request"]
        except KeyError as e:
            raise ValidationError("O request precisa estar no contexto.", code="invalid") from e

        try:
            _ = request.user
        except (KeyError, AttributeError) as e:
            raise ValidationError("O user precisa estar no contexto.", code="invalid") from e

        return super().validate(attrs)


class PaymentSerializer(serializers.ModelSerializer):

    loan = serializers.UUIDField(source="loan.uuid")

    class Meta:
        model = Payment
        fields = (
            "uuid",
            "value",
            "loan",
            "created_at",
            "modified_at",
        )

        extra_kwargs = {
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True},
        }

    def validate(self, attrs):

        attrs = super().validate(attrs)

        try:
            request = self.context["request"]
        except KeyError as e:
            raise ValidationError("O request precisa estar no contexto.", code="invalid") from e

        try:
            user = request.user
        except (KeyError, AttributeError) as e:
            raise ValidationError("O user precisa estar no contexto.", code="invalid") from e

        loan = attrs["loan"]["uuid"]
        try:
            loan = Loan.objects.get(uuid=loan, user=user)
        except Loan.DoesNotExist as e:
            raise ValidationError(
                {"loan": f'Pk inválido "{loan}" - objeto não existe.'},
                code="does_not_exist",
            ) from e

        attrs["loan"] = loan

        return attrs
