from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Payment(models.Model):
    class PaymentType(models.TextChoices):
        DEBIT = 'DB', _('DEBIT')
        CREDIT_CARD = 'CD', _('CREDIT_CARD')

    type = models.CharField(max_length=2, choices=PaymentType.choices, default=PaymentType.DEBIT)
    is_paid = models.BooleanField()