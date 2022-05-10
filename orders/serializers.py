from rest_framework import serializers
from products.models import Product
from products.serializers import ProductSerializer
from .models import Order, OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'order_id', 'product_id', 'quantity']
        read_only_fields = ['id']

    
    def create(self, validated_data):
        # custom creation method to check if OrderProduct's product has stock

        # get the Product serializer to access the stock_quantity field
        product_serializer = ProductSerializer(instance=validated_data['product_id'])

        # if the Product does not have the desired quantity, throws validation error
        if validated_data['quantity'] > product_serializer.data['stock_quantity']:
            raise serializers.ValidationError({'quantity': ['Product has no stock']})

        # save the OrderProduct object
        order_product = OrderProduct.objects.create(**validated_data)

        return order_product        


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ['id', 'price', 'user_id', 'payment_id', 'products', 'created']
        read_only_fields = ['id', 'created']
        

    def create(self, validated_data):
        # custom creation method to allow creating OrderProducts on Orders create method

        products_data = validated_data.pop('products', None)
        order = Order.objects.create(**validated_data)

        if products_data is not None:
            for product_data in products_data:
                OrderProduct.objects.create(order_id=order, **product_data)

        return order


    def update(self, instance, validated_data):
        # custom update method to don't update OrderProducts when trying to update an Order
        
        instance.price = validated_data.get('price', instance.price)
        instance.payment_id = validated_data.get('payment_id', instance.payment_id)
        instance.user_id = validated_data.get('user_id', instance.user_id)
        instance.save()

        return instance
