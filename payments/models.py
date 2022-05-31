from xml.dom.expatbuilder import parseString
from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _


class Payment(models.Model):
    class Type(models.TextChoices):
        SALE = 'SALE', _('Sale Payment')
        CASH_REGISTER = 'CHRG', _('CashRegister Payment')

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=4, choices=Type.choices, default=Type.SALE)
    is_paid = models.BooleanField(blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_type(self):
        return self.Type(self.type).label


class CashRegister(models.Model):
    details = models.TextField(null=True, blank=True)
    initial_amount = models.DecimalField(max_digits=10, decimal_places=2)
    closed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    open = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.details


class Transaction(models.Model):

    class Type(models.TextChoices):
        CASH = 'CI', _('Deposit')
        CASH_BACK = 'CB', _('Cashback')


    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    cash_register = models.ForeignKey(CashRegister, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.CASH)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    details = models.TextField(null=True, blank=True)

    def get_type(self):
        return self.Type(self.type).label