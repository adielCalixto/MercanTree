from rest_framework import serializers
from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order_id', 'product_id', 'quantity']
        read_only_fields = ['id', 'order_id']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False, default=[])

    class Meta:
        model = Order
        fields = ['id', 'value', 'user_id', 'payment_id', 'products']
        read_only_fields = ['id']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product_data in products_data:
            OrderProduct.objects.create(order_id=order, **product_data)
        return order


    def update(self, instance, validated_data):
        instance.value = validated_data.get('value', instance.value)
        instance.payment_id = validated_data.get('payment_id', instance.payment_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()

        return instance
