from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Sum

from app.core.models import Loan

ZERO = Decimal("0.00")


@dataclass(frozen=True)
class DebtLoan:
    total: Decimal
    interest: Decimal


class TotalPaymentLoanNotFound(Exception):
    def __init__(self, uuid):
        super().__init__(self, f'Emprestimo com o "{uuid}" não existe.')


def extract_client_id(meta: dict) -> str:
    """Obtem o IP do cliente.

    Args:
        meta (dict): Meta dados do resquest do django

    Returns:
        str: o ipv4 ou ipv6 do cliente.
    """

    if x_forwared_for := meta.get("HTTP_X_FORWARDED_FOR"):
        ip = x_forwared_for.split(",")[0].strip()
    else:
        ip = meta.get("REMOTE_ADDR")

    return ip


def total_payment_for_the_loan(loan: Loan) -> Decimal:
    """Calcula o total já pago para um determinado emprestimo

    Args:
        loan: Emprestimo

    Returns:
        Decimal: Soma do valor total pago.
    """

    return loan.payments.aggregate(total=Sum("value", default=ZERO))["total"]


# TODO: O código esta com problema de perda precisão verifiacar isso depois
def loan_with_interest(
    principal: Decimal,
    rate: Decimal,
    period: int,
    compound_interest: bool = False,
) -> DebtLoan:
    """Calcula o montante final e juros do um emprestimo.

    Args:
        principal (Decimal): Valor inicial do emprestimo.
        rate (Decimal): taxa mensal de juros em porcentagem.
        period (datetime): Numero de Periodos.
        compound_interest (bool, optional): Calculo de jutos compostos. Defaults to False.

    Returns:
        DebtLoan: Retorna o montante final e o juros do emprestimo.
    """

    rate_decimal = rate / 100
    if compound_interest:
        debt_total = principal * (1 + rate_decimal) ** period
        total_interest = debt_total - principal
    else:
        total_interest = principal * rate_decimal * period
        debt_total = principal + total_interest

    return DebtLoan(total=round(debt_total, 2), interest=round(total_interest, 2))
