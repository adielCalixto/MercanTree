from rest_framework import serializers
from .models import Supplier, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'barcode', 'expires_at', 'price', 'category', 'quantity', 'supplier_id', 'supplier_price']
        read_only_fields = ['id']


class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'cnpj', 'responsable', 'address', 'city']
        read_only_fields = ['id']