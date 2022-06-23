from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db import models
import uuid
from users.models import User
from products.models import StockProduct, StockProductTrackingCode
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

    
    def __str__(self):
        return self.code


class Order(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PD', _('Pending')
        CANCELED = 'CC', _('Canceled')
        DONE = 'DN', _('Done')


    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.PENDING, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    coupon = models.ForeignKey(Coupon, blank=True, to_field='code', null=True, on_delete=models.SET_NULL)
    details = models.TextField(null=True, blank=True)

    def get_status(self):
        return self.Status(self.status).label

    
    def __str__(self):
        username = self.user.username if self.user else 'User deleted'
        return "User: %s, at: %s, status: %s" % (username, self.created, self.Status(self.status).label)


class OrderProduct(models.Model):
    uid = models.CharField(max_length=100, primary_key=True, default=uuid.uuid4, unique=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    product = models.ForeignKey(StockProduct, on_delete=models.SET_NULL, null=True, blank=True)
    sale_quantity = models.DecimalField(max_digits=10, decimal_places=4, null=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=True)
    reference = models.CharField(max_length=100, null=False, blank=True)

    def clean(self):
        if self.product:
            if not self.reference:
                self.reference = self.product.product.name
            if not self.sale_price:
                self.sale_price = self.product.price

            old_obj = None

            try:
                old_obj = OrderProduct.objects.get(pk=self.uid)
            except:
                pass

            if self.sale_quantity > self.product.quantity + (old_obj.sale_quantity if old_obj else 0):
                raise ValidationError('Quantity not available on stock')


    def __str__(self):
        return "%s - %d x $%d" % (self.reference, self.sale_quantity, self.sale_price)


    def return_order_product(self, user, notes=None):
        if self.product:
            self.product.addQuantity(self.sale_quantity, user, notes, StockProductTrackingCode.STOCK_RETURNED)

        self.delete()

    
    def save(self, *args, **kwargs):
        self.clean()

        super().save(*args, **kwargs)


@receiver(post_save, sender=OrderProduct)
def update_stock_product_quantity(sender, instance, created, **kwargs):
    if created and instance.product != None:
        instance.product.removeQuantity(instance.sale_quantity)