from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(trim_whitespace=False, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"),
                username=email,
                password=password,
            )

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = "Não é possível fazer login com as credenciais fornecidas."
                raise serializers.ValidationError(msg, code="authorization")
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user

        return attrs


class WhoamiSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "created_at",
            "modified_at",
        )
        extra_kwargs = {
            "name": {"read_only": True},
            "email": {"read_only": True},
            "created_at": {"read_only": True},
            "modified_at": {"read_only": True},
        }
