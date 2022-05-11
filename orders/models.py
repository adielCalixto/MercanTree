from django.db import models
from users.models import User
from products.models import Product
from payments.models import Payment


COUPON_CHOICES = (
    ('PC', 'PERCENT'),
    ('AM', 'AMOUNT'),
)


class Coupon(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    discount = models.FloatField()
    type = models.CharField(max_length=2, choices=COUPON_CHOICES, default="AM", blank=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, blank=True, to_field='code', null=True, on_delete=models.SET_NULL)


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products', blank=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False)