from decimal import Decimal
from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum
from django.utils.functional import cached_property

from app.accounts.models import CreationModificationBase
from app.core.services import loan_with_interest

DECIMAL_MAX_DIGITS = 14
DECIMAL_PLACES = 2
ZERO = Decimal("0.00")


class Loan(CreationModificationBase, models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    value = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        validators=[MinValueValidator(0.00)],
    )
    rate = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        validators=[MinValueValidator(0.00)],
    )
    contracted_period = models.PositiveSmallIntegerField()
    register_ip = models.GenericIPAddressField()
    bank = models.CharField(max_length=100)
    request_date = models.DateField()

    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="loans")

    def __str__(self):
        return str(self.uuid)

    @cached_property
    def value_with_interest(self):
        return loan_with_interest(self.value, self.rate, self.contracted_period)

    @property
    def amount_due(self):
        return self.value_with_interest.total - self.total_payments

    @property
    def total_payments(self):
        """Calcula o total já pago para um determinado emprestimo
        Returns:
            Decimal: Soma do valor total pago.
        """
        return self.payments.aggregate(total=Sum("value", default=ZERO))["total"]


class Payment(CreationModificationBase, models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING, related_name="payments")
    value = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, validators=[MinValueValidator(0.00)]
    )
    payment_date = models.DateField()

    def __str__(self):
        return str(self.uuid)
