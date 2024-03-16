import uuid
from decimal import Decimal

from django.db.models import Sum

from app.core.models import Loan

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


def total_payment_for_the_loan(uuid: uuid) -> Decimal:
    """Calcula o total já pago para um determinado emprestimo

    Args:
        uuid (uuid): Identificador unico do emprestimo

    Raises:
        TotalPaymentLoanNotFound: Retorna um erro caso o emprestimo não seja achado.

    Returns:
        Decimal: Soma do valor total pago.
    """

    try:
        loan = Loan.objects.get(uuid=uuid)
    except Loan.DoesNotExist as e:
        raise TotalPaymentLoanNotFound(uuid) from e

    return loan.payments.aggregate(total=Sum("value", default=ZERO))["total"]
