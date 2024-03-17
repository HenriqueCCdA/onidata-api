from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated

from app.core.models import Payment
from app.core.permission import UserOnlyCanAccessOwnPayment
from app.core.serializers import PaymentSerializer


@extend_schema(tags=["Pagamentos"])
class PaymentLC(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(loan__user=self.request.user)

    @extend_schema(summary="Lista de pagamentos")
    def get(self, request, *args, **kwargs):
        """Retorna os pagamentos usuario. O usuario é
        obtido pelo `Token`. O pagamento é definido pelo seu `uuid`.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Cria o pagamento para um emprestimo")
    def post(self, request, *args, **kwargs):
        """Cria o pagamento para emprestimo. O usuario é
        obtido pelo `Token`. O pagamento é definido pelo seu `uuid`.
        """
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["Pagamentos"])
class PaymentRetrieve(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (UserOnlyCanAccessOwnPayment, IsAuthenticated)
    lookup_field = "uuid"
    lookup_url_kwarg = "id"

    @extend_schema(summary="Recupera um pagamento")
    def get(self, request, *args, **kwargs):
        """Recupera um pagamento do usuario. O usuario é
        obtido pelo `Token`. O pagamento é definido pelo seu `uuid`.
        """
        return super().get(request, *args, **kwargs)


payment_lc = PaymentLC.as_view()
payment_retrieve = PaymentRetrieve.as_view()
