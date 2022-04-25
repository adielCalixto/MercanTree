from rest_framework import serializers
from .models import Order, OrderProduct


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['value', 'user_id', 'payment_id']


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['order_id', 'product_id', 'quantity']