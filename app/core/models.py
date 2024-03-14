from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from app.accounts.models import CreationModificationBase


class Loan(CreationModificationBase, models.Model):

    uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
    nominal_value = models.DecimalField(max_digits=14, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=14, decimal_places=2)
    register_ip = models.GenericIPAddressField()
    bank = models.CharField(max_length=100)

    user = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, related_name="loans")

    def __str__(self):
        return f"loan(uuid={self.uuid},value={self.nominal_value})"
