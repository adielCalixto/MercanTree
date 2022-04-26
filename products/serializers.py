from rest_framework import serializers
from .models import Supplier, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'description', 'barcode', 'expires_at', 'price', 'category', 'supplier_id']

class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'phone', 'cnpj', 'responsable', 'address', 'city']