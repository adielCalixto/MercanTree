from django.db import models
from users.models import User
from products.models import Product
from payments.models import Payment


class Order(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    payment_id = models.ForeignKey(Payment, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products', blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(null=False)