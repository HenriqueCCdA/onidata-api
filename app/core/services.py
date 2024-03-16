from decimal import Decimal

from django.db.models import Sum

ZERO = Decimal("0.00")


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


def total_payment_for_the_loan(loan) -> Decimal:
    """Calcula o total já pago para um determinado emprestimo

    Args:
        loan: Emprestimo

    Returns:
        Decimal: Soma do valor total pago.
    """

    return loan.payments.aggregate(total=Sum("value", default=ZERO))["total"]
