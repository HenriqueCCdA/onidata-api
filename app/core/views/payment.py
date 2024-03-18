from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from app.core.models import Payment
from app.core.permission import UserOnlyCanAccessOwnPayment
from app.core.serializers import PaymentSerializer


@extend_schema_view(
    get=extend_schema(
        tags=["Pagamentos"],
        summary="Lista de pagamentos",
        description=(
            "Retorna os pagamentos de usuário. O usuario é obtido pelo `Token`. "
            "O pagamento é definido pelo seu `uuid`."
        ),
    ),
    post=extend_schema(
        tags=["Pagamentos"],
        summary="Cria o pagamento para um emprestimo",
        description=(
            "Cria o pagamento para emprestimo para um usuário. O usuario é obtido pelo `Token`. "
            "O pagamento é definido pelo seu `uuid`."
        ),
    ),
)
class PaymentLC(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(loan__user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        tags=["Pagamentos"],
        summary="Recupera um pagamento",
        description=(
            "Recupera um pagamento de um usuário. O usuario é obtido pelo `Token`. "
            "O pagamento é definido pelo seu `uuid`."
        ),
    ),
)
class PaymentRetrieve(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (UserOnlyCanAccessOwnPayment, IsAuthenticated)
    lookup_field = "uuid"
    lookup_url_kwarg = "id"


payment_lc = PaymentLC.as_view()
payment_retrieve = PaymentRetrieve.as_view()
