from django.db import models


CHARGE_CHOICES = (
    ('CD', 'CashDeposit'),
)


class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class PaymentCharge(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=2, choices=CHARGE_CHOICES)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.payment.is_paid == True:
            return
        else:
            super().save(*args, **kwargs)  # Call the "real" save() method.