from uuid import uuid4

from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from app.accounts.models import CreationModificationBase

# TODO: Estou usando o created_at com data de solicitaçao e pagammento,
# não tenho certeza se isso é bom. Pensar mellhor nisso depois


class Loan(CreationModificationBase, models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    nominal_value = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0.00)])
    interest_rate = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0.00)])
    register_ip = models.GenericIPAddressField()
    bank = models.CharField(max_length=100)

    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="loans")

    def __str__(self):
        return f"loan(uuid={self.uuid},value={self.nominal_value})"


class Payment(CreationModificationBase, models.Model):

    loan = models.ForeignKey(Loan, on_delete=models.DO_NOTHING, related_name="payments")
    value = models.DecimalField(max_digits=14, decimal_places=2, validators=[MinValueValidator(0.00)])

    def __str__(self):
        return f"payment(id={self.id},loan_uuid={self.loan.uuid},value={self.value})"
