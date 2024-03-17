from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from django.db.models import Sum

from app.core.models import Loan

ZERO = Decimal("0.00")
DAYS_IN_MONTH = 30


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
    interest_rate: Decimal,
    initial_date: datetime,
    current_date: datetime,
    compound_interest: bool = False,
) -> DebtLoan:
    """Calcula o montante final e juros do um emprestimo

    Args:
        principal (Decimal): Valor inicial do emprestimo
        interest_rate (Decimal): taxa mensal de juros em porcentagem_
        initial_date (datetime): Data inicial do emprestimo
        current_date (datetime):  Data atual
        compound_interest (bool, optional): Calculo de jutos compostos. Defaults to False.

    Returns:
        DebtLoan: Retorna o montante final e o juros do emprestimo.
    """

    interest_rate_decimal = interest_rate / 100
    delta_time = current_date - initial_date
    if compound_interest:
        interest_rate_day = (1 + Decimal(interest_rate_decimal)) ** (Decimal(1 / DAYS_IN_MONTH)) - 1
        debt_total = principal * (1 + interest_rate_day) ** delta_time.days
        total_interest = debt_total - principal
    else:
        interest_rate_day = interest_rate_decimal / DAYS_IN_MONTH
        total_interest = principal * interest_rate_day * delta_time.days
        debt_total = principal + total_interest

    return DebtLoan(total=round(debt_total, 2), interest=round(total_interest, 2))
