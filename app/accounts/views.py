from drf_spectacular.utils import extend_schema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.accounts.serializers import MyAuthTokenSerializer, WhoamiSerializer


class MyObtainAuthToken(ObtainAuthToken):
    """
    Retorna o **Token** do usuário.

    - email
    - password
    """

    parser_classes = (JSONParser,)
    serializer_class = MyAuthTokenSerializer


class Whoami(APIView):
    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=WhoamiSerializer)
    def get(self, request):
        """Retorna o usuário que pertence o **Token**"""
        user = request.user

        serialize = WhoamiSerializer(instance=user)

        return Response(serialize.data)


obtain_auth_token = MyObtainAuthToken.as_view()
whoiam = Whoami.as_view()
