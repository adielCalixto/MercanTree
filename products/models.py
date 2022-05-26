from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    cnpj = models.CharField(max_length=14, null=True, blank=True)
    responsable = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    barcode = models.CharField(max_length=255)
    expires_at = models.DateTimeField('Date of expiration')
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    supplier_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    quantity = models.IntegerField(null=False, default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
