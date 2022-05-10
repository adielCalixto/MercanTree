from rest_framework import serializers
from .models import Supplier, Product
from django.db.models import Sum
from orders.models import OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'barcode', 'expires_at', 'price', 'category', 'quantity', 'stock_quantity', 'supplier_id', 'supplier_price']
        read_only_fields = ['id']

    
    def get_stock_quantity(self, obj):
        product_count = obj.quantity
        in_order_count = OrderProduct.objects.filter(product_id=obj.id).aggregate(Sum('quantity'))
        count = product_count - (in_order_count['quantity__sum'] if in_order_count['quantity__sum'] else 0)

        return count


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'cnpj', 'responsable', 'address', 'city']
        read_only_fields = ['id']