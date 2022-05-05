from ast import Or
from rest_framework import serializers

from products.models import Product
from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order_id', 'product_id', 'quantity']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'price', 'user_id', 'payment_id', 'products']
        read_only_fields = ['id']
        

    def create(self, validated_data):
        products_data = validated_data.pop('products', None)
        order = Order.objects.create(**validated_data)

        if products_data is not None:
            for product_data in products_data:
                OrderProduct.objects.create(order_id=order, **product_data)

        return order


    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        instance.payment_id = validated_data.get('payment_id', instance.payment_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()

        return instance
