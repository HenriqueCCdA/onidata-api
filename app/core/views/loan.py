from dataclasses import asdict

from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view
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


@extend_schema(tags=["Emprestimos"])
@extend_schema_view(
    get=extend_schema(
        tags=["Emprestimos"],
        summary="Lista os emprestimo",
        description=(
            "Retorna os emprestimos do usuario logado. O usuario é obtido pelo `Token`. "
            "O emprestimo é definido pelo seu `uuid`.."
        ),
    ),
    post=extend_schema(
        tags=["Emprestimos"],
        summary="Lista os emprestimo",
        description=(
            "Cria o emprestimo do usuario autorizado. O usuario é obtido pelo `Token`. "
            "O emprestimo é definido pelo seu `uuid`.."
        ),
    ),
)
class LoansLCView(ListCreateAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


@extend_schema_view(
    get=extend_schema(
        tags=["Emprestimos"],
        summary="Recupera um emprestimo",
        description=(
            "Recupera um emprestimo do usuario. O usuario é obtido pelo Token. "
            "O emprestimo é definido pelo seu `uuid`."
        ),
    ),
)
class LoanRetrieveView(RetrieveAPIView):
    serializer_class = LoanSerializer
    queryset = Loan.objects.all()
    permission_classes = (UserOnlyCanAccessOwnLoan, IsAuthenticated)
    lookup_field = "uuid"
    lookup_url_kwarg = "id"


@extend_schema(tags=["Juros, pagamentos e valores devidos"])
class LoanPaymentListView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = (UserOnlyCanAccessOwnPayment, IsAuthenticated)

    @extend_schema(summary="Lista de pagamentos do emprestimo")
    def get(self, request, id):
        """Lista de pagamentos de um emprestimo específico.
        O emprestimo é definido pelo seu `uuid`.
        """
        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)
        payments = loan.payments.all()
        serialize = PaymentSerializer(instance=payments, many=True)

        return Response(serialize.data)


class LoanPaymentSumView(APIView):
    serializer_class = PaymentSumSerializer

    @extend_schema(tags=["Juros, pagamentos e valores devidos"], summary="Soma os pamentos de um emprestimo")
    def get(self, request, id):
        """
        Soma os pagamentos feitos para um emprestimo específico.
        O emprestimo é definido pelo seu `uuid`.
        """

        loan = get_object_or_404(Loan, uuid=id, user=self.request.user)

        serialize = PaymentSumSerializer(data={"total": loan.total_payments})
        serialize.is_valid(raise_exception=True)

        return Response(serialize.data)


class LoanWithInterestView(APIView):
    serializer_class = DebtLoanSerializer

    @extend_schema(tags=["Juros, pagamentos e valores devidos"], summary="Calcula montente fianl e juros")
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


class AmountDueView(APIView):
    serializer_class = AmountDueSerializer

    @extend_schema(tags=["Juros, pagamentos e valores devidos"], summary="Valor devido")
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
