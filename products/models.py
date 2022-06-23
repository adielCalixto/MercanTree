from django.db import models
from users.models import User
from django.utils.translation import gettext_lazy as _

class StockProductTrackingCode(models.TextChoices):
    STOCK_ADD = '10', _('Stock added')
    STOCK_REMOVE = '11', _('Stock removed')
    STOCK_RETURNED = '12', _('Stock returned')
    STOCK_EDITED = '13', _('Stock edited')


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    cnpj = models.CharField(max_length=14, null=True, blank=True)
    responsable = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)


    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    barcode = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(null=False, blank=True, default=True)
    units = models.CharField(
        max_length=20, default="",
        blank=True, null=True
    )

    def delete(self):
        # don't let the product be deleted from the database, just set it as inactive
        self.active = False
        self.save()


    def __str__(self):
        barcode = self.barcode if self.barcode else '0000'
        return "%s - %s" % (self.name, barcode)


class StockProduct(models.Model):
    product = models.ForeignKey(Product, null=False, blank=False, on_delete=models.DO_NOTHING)
    expires_at = models.DateField('Date of expiration', null=True, blank=True)
    delete_on_deplete = models.BooleanField(default=False, null=False, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False, verbose_name="Purchase Price")
    quantity = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Stock of: %s" % self.product.name

    
    def updateQuantity(self, quantity):
        if quantity < 0:
            quantity = 0

        self.quantity = quantity

        if quantity == 0 and self.delete_on_deplete:
            self.delete()
            return False
        else:
            self.save()
            return True

    
    def addTrackingEntry(self, code, user, notes, deltas):
        entry = StockProductTracking.objects.create(
            code=code,
            user=user,
            product=self,
            notes=notes,
            deltas=deltas
        )

        entry.save()

    
    def removeQuantity(self, quantity, user=None, notes=None, code = StockProductTrackingCode.STOCK_REMOVE):
        if quantity <= 0:
            return False

        if self.updateQuantity(self.quantity - quantity):
            self.addTrackingEntry(
                code,
                user,
                notes,
                deltas={
                    'removed': float(quantity),
                    'quantity': float(self.quantity),
                }
            )
        
        return True


    def addQuantity(self, quantity, user=None, notes=None, code = StockProductTrackingCode.STOCK_ADD):
        if quantity <= 0:
            return False        

        if self.updateQuantity(self.quantity + quantity):
            self.addTrackingEntry(
                code,
                user,
                notes,
                deltas={
                    'added': float(quantity),
                    'quantity': float(self.quantity),
                }
            )
        
        return True

    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class StockProductTracking(models.Model):
    code = models.CharField(max_length=2, choices=StockProductTrackingCode.choices)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(StockProduct, null=False, blank=False, on_delete=models.CASCADE)
    deltas = models.JSONField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)