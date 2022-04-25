from django.db import models
from users.models import User
from products.models import Product
from payments.models import Payment


class Order(models.Model):
    value = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    payment_id = models.ForeignKey(Payment, on_delete=models.DO_NOTHING)


class OrderProduct(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField()