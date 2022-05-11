from rest_framework import serializers
from products.serializers import ProductSerializer
from .models import Order, OrderProduct, Coupon


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order', 'product', 'quantity']
        read_only_fields = ['id']

    
    def create(self, validated_data):
        # custom creation method to check if OrderProduct's product has stock

        # get the Product serializer to access the stock_quantity field
        product_serializer = ProductSerializer(instance=validated_data['product'])

        # if the Product does not have the desired quantity, throws validation error
        if validated_data['quantity'] > product_serializer.data['stock_quantity']:
            raise serializers.ValidationError({'quantity': ['Product has no stock']})

        # save the OrderProduct object
        order_product = OrderProduct.objects.create(**validated_data)

        return order_product        


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'created', 'payment', 'coupon']
        read_only_fields = ['id', 'created']
        

class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon
        fields = ('code', 'type', 'discount')