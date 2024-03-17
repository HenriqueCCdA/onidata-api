from dataclasses import asdict

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.core.models import Loan
from app.core.permission import UserOnlyCanAccessOwnLoan, UserOnlyCanAccessOwnPayment
from app.core.serializers import (
    AmountDueSerializer,
    DebtLoanSerializer,
    LoanSerializer,
    PaymentSerializer,
    PaymentSumSerializer,
)
from app.core.services import loan_with_interest as loan_with_interest_
from app.core.services import total_payment_for_the_loan


@extend_schema(tags=["Emprestimos"])
class LoansLCView(ListCreateAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    @extend_schema(summary="Lista os emprestimo")
    def get(self, request, *args, **kwargs):
        """Retorna os emprestimos do usuario logado. O usuario é
        obtido pelo `Token`. O emprestimo pe definido pelo seu `uuid`.
        """
        return super().get(request, *args, **kwargs)

    @extend_schema(summary="Cria o emprestimo")
    def post(self, request, *args, **kwargs):
        """Cria o emprestimo do usuario auth. O usuario é
        obtido pelo `Token`. O emprestimo pe definido pelo seu `uuid`.
        """
        return super().post(request, *args, **kwargs)


@extend_schema(tags=["Emprestimos"])
class LoanRetrieveView(RetrieveAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    permission_classes = (UserOnlyCanAccessOwnLoan, IsAuthenticated)
    lookup_field = "uuid"
    lookup_url_kwarg = "id"

    @extend_schema(summary="Recupera um emprestimo")
    def get(self, request, *args, **kwargs):
        """Recupera um emprestimo do usuario. O usuario é
        obtido pelo Token. O emprestimo pe definido pelo seu `uuid`.
        """
        return super().get(request, *args, **kwargs)


@extend_schema(tags=["Juros, pagementos e valores devidos"])
class LoanPaymentListView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = (UserOnlyCanAccessOwnPayment, IsAuthenticated)

    @extend_schema(summary="Lista de pagamentos do emprestimo")
    def get(self, request, id):
        """Lista de pagamentos de um emprestimo específico.
        O emprestimo pe definido pelo seu `uuid`.
        """
        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)
        payments = loan.payments.all()
        serialize = PaymentSerializer(instance=payments, many=True)

        return Response(serialize.data)


@extend_schema(tags=["Juros, pagementos e valores devidos"])
class LoanPaymentSumView(APIView):
    serializer_class = PaymentSumSerializer

    @extend_schema(summary="Soma os pamentos de um emprestimo")
    def get(self, request, id):
        """
        Soma os pagamentos feitos para um emprestimo específico.
        O emprestimo é definido pelo seu `uuid`.
        """

        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)

        total = total_payment_for_the_loan(loan)

        serialize = PaymentSumSerializer(data={"total": total})
        serialize.is_valid(raise_exception=True)

        return Response(serialize.data)


@extend_schema(tags=["Juros, pagementos e valores devidos"])
class LoanWithInterestView(APIView):
    serializer_class = DebtLoanSerializer

    @extend_schema(summary="Calcula montente fianl e juros")
    def get(self, request, id):
        """
        Calcula o montante final e o juros de um emprestimos especifico.
        O emprestimo é definido pelo seu `uuid`. O calculo e feito com juros simples pode padrão
        Para usar juros composto basta usar a query string `interest=compound`
        """

        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)

        compound_interest = False
        if self.request.query_params.get("interest") == "compound":
            compound_interest = True

        result = loan_with_interest_(loan.value, loan.rate, loan.contracted_period, compound_interest=compound_interest)

        serialize = DebtLoanSerializer(data=asdict(result))
        serialize.is_valid(raise_exception=True)

        return Response(serialize.data)


@extend_schema(tags=["Juros, pagementos e valores devidos"])
class AmountDueView(APIView):
    serializer_class = AmountDueSerializer

    @extend_schema(summary="Valor devido")
    def get(self, request, id):
        """Total do valor devido com os pagamentos já descontados. O emprestimo é definido pelo seu `uuid`.
        O calculo e feito com juros simples.
        """

        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)

        serialize = AmountDueSerializer(data={"due": loan.amount_due})
        serialize.is_valid(raise_exception=True)

        return Response(serialize.data)


loan_lc = LoansLCView.as_view()
loan_retrieve = LoanRetrieveView.as_view()
loan_payment_list = LoanPaymentListView.as_view()
loan_payment_sum = LoanPaymentSumView.as_view()
loan_with_interest = LoanWithInterestView.as_view()
loan_amount_due = AmountDueView.as_view()
