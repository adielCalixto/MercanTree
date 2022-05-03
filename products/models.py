from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    cnpj = models.CharField(max_length=14, null=True)
    responsable = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    barcode = models.CharField(max_length=255)
    expires_at = models.DateTimeField('date of expiration')
    price = models.FloatField()
    category = models.CharField(max_length=100)
    supplier_id = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
