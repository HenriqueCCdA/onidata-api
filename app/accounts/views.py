from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.serializers import MyAuthTokenSerializer, WhoamiSerializer


@extend_schema_view(
    post=extend_schema(
        summary="Login do usuário",
    ),
)
class MyObtainAuthToken(ObtainAuthToken):
    """
    Retorna o **Token** do usuário.

    - email
    - password

    `Infos`: Foi utilizazdo o `AuthToken`.
    """

    parser_classes = (JSONParser,)
    serializer_class = MyAuthTokenSerializer


class Whoami(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = WhoamiSerializer

    @extend_schema(summary="Testa a autenticação.")
    def get(self, request):
        """Retorna o usuário que pertence o **Token** passado no cabeçalho darequisição.

        O Token quem que ser passado como:

        `Authorization: Token 8dfc6fbccdd5316a9ddcbdca6c8252e78f1c0cfc`


        """
        user = request.user

        serialize = WhoamiSerializer(instance=user)

        return Response(serialize.data)


obtain_auth_token = MyObtainAuthToken.as_view()
whoiam = Whoami.as_view()
