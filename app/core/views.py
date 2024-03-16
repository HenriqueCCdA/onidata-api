from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.models import Loan, Payment
from app.core.permission import UserOnlyCanAccessOwnLoan, UserOnlyCanAccessOwnPayment
from app.core.serializers import LoanSerializer, PaymentSerializer, PaymentSumSerializer
from app.core.services import extract_client_id, total_payment_for_the_loan


@extend_schema(tags=["debug"])
@api_view(["GET"])
@permission_classes([])
def get_client_ip(request):
    """Retorna o IP do client"""
    return Response({"client_ip": extract_client_id(request.META)})


class LoansLC(ListCreateAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    @extend_schema(summary="Lista os emprestimo")
    def get(self, request, *args, **kwargs):
        """Retorna os emprestimos do usuario logado. O usuario é
        obtido pelo Token.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Cria o emprestimo")
    def post(self, request, *args, **kwargs):
        """Cria o emprestimo do usuario auth. O usuario é
        obtido pelo Token.
        """
        return super().post(request, *args, **kwargs)


class LoanRetrieve(RetrieveAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    permission_classes = (UserOnlyCanAccessOwnLoan, IsAuthenticated)
    lookup_field = "uuid"
    lookup_url_kwarg = "id"

    @extend_schema(summary="Recupera um emprestimo")
    def get(self, request, *args, **kwargs):
        """Recupera um emprestimo do usuario. O usuario é
        obtido pelo Token.
        """
        return super().get(request, *args, **kwargs)


class LoanPaymentList(APIView):
    serializer_class = PaymentSerializer
    permission_classes = (UserOnlyCanAccessOwnPayment, IsAuthenticated)

    def get(self, request, id):
        """List do pagamentos de um emprestimo especifico"""
        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)
        payments = loan.payments.all()
        serialize = PaymentSerializer(instance=payments, many=True)

        return Response(serialize.data)


class LoanPaymentSum(APIView):
    serializer_class = PaymentSumSerializer

    def get(self, request, id):
        """Soma os pagamentos feitos para um emprestimo especifico"""

        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)

        total = total_payment_for_the_loan(loan)

        serialize = PaymentSumSerializer(data={"total": total})
        serialize.is_valid(raise_exception=True)

        return Response(serialize.data)


class PaymentLC(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(loan__user=self.request.user)

    @extend_schema(summary="Lista de pagamentos")
    def get(self, request, *args, **kwargs):
        """Retorna os pagamentos usuario. O usuario é
        obtido pelo Token.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Cria o pagamento para um emprestimo")
    def post(self, request, *args, **kwargs):
        """Cria o pagamento para emprestimo.O usuario é
        obtido pelo Token.
        """
        return super().post(request, *args, **kwargs)


class PaymentRetrieve(RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = (UserOnlyCanAccessOwnPayment, IsAuthenticated)

    @extend_schema(summary="Recupera um pagamento")
    def get(self, request, *args, **kwargs):
        """Recupera um pagamento do usuario. O usuario é
        obtido pelo Token.
        """
        return super().get(request, *args, **kwargs)


loans_lc = LoansLC.as_view()
loan_retrieve = LoanRetrieve.as_view()
loan_payment_list = LoanPaymentList.as_view()
loan_payment_sum = LoanPaymentSum.as_view()

payment_lc = PaymentLC.as_view()
payment_retrieve = PaymentRetrieve.as_view()
