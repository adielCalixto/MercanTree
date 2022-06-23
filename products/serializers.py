from rest_framework import serializers
from .models import Category, StockProduct, Supplier, Product
from rest_flex_fields import FlexFieldsModelSerializer

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField('name', queryset=Category.objects.all(), allow_null=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'barcode', 'category']
        read_only_fields = ['id']


class StockProductSerializer(FlexFieldsModelSerializer):
    
    class Meta:
        model = StockProduct
        fields = '__all__'
        read_only_fields = ['id']
        expandable_fields = {
            'product': ProductSerializer
        }


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'cnpj', 'responsable', 'address', 'city']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        read_only_fields = ['id']