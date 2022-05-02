from rest_framework import serializers
from .models import Order, OrderProduct


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'value', 'user_id', 'payment_id']
        read_only_fields = ['id']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order_id', 'product_id', 'quantity']
        read_only_fields = ['id']