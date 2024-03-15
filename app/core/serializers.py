from django.forms import ValidationError
from rest_framework import serializers

from app.core.models import Loan
from app.core.services import extract_client_id


class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = (
            "uuid",
            "nominal_value",
            "interest_rate",
            "register_ip",
            "bank",
            "created_at",
            "modified_at",
        )

        extra_kwargs = {
            "uuid": {"read_only": True},
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True},
            "register_ip": {"read_only": True},
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
