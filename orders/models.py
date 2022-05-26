from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid
from users.models import User
from products.models import Product
from payments.models import Payment


class Coupon(models.Model):

    class Type(models.TextChoices):
        PERCENT = 'PC', _('Percent')
        AMOUNT = 'AM', _('Amount')


    code = models.CharField(max_length=15, primary_key=True)
    discount = models.FloatField()
    type = models.CharField(max_length=2, choices=Type.choices, default=Type.AMOUNT)

    def get_type(self):
        return self.Type(self.type).label


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PD', _('Pending')
        CANCELED = 'CC', _('Canceled')
        DONE = 'DN', _('Done')


    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, blank=True, to_field='code', null=True, on_delete=models.SET_NULL)
    details = models.TextField(null=True, blank=True)

    def get_status(self):
        return self.Status(self.status).label


class OrderProduct(models.Model):
    id = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, unique=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False)