from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from app.accounts.models import CreationModificationBase

# TODO: Estou usando o created_at com data de solicitaçao e pagammento,
# não tenho certeza se isso é bom. Pensar mellhor nisso depois

DECIMAL_MAX_DIGITS = 14
DECIMAL_PLACES = 2


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

    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="loans")

    def __str__(self):
        return str(self.uuid)


class Payment(CreationModificationBase, models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING, related_name="payments")
    value = models.DecimalField(
        max_digits=DECIMAL_MAX_DIGITS, decimal_places=DECIMAL_PLACES, validators=[MinValueValidator(0.00)]
    )

    def __str__(self):
        return str(self.uuid)
