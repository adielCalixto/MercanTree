import uuid
from rest_framework import serializers
from payments.serializers import PaymentSerializer
from products.serializers import ProductSerializer
from .models import Order, OrderProduct, Coupon
from payments.models import Payment
from rest_flex_fields import FlexFieldsModelSerializer


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = '__all__'
        extra_kwargs = {
            'order': {
                'write_only': True,
            },
            'id': {
                'validators': []
            }
        }
    

    def create(self, validated_data):        
        # pop id, since it should be generated automatically
        validated_data.pop('id', None)

        # create order_product
        order_product = OrderProduct.objects.create(**validated_data)
        return order_product


    def update(self, instance, validated_data):        
        # pop id, since it should not be updated
        validated_data.pop('id', None)

        # create order_product
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.order = validated_data.get('order', instance.order)
        instance.save()

        return instance


    def validate(self, data):
        # custom validation method to check if OrderProduct's product has stock

        # get the Product serializer to access the stock_quantity field
        product_serializer = ProductSerializer(instance=data['product'])

        # if the Product does not have the desired quantity, throws validation error
        if data['quantity'] > product_serializer.data['stock_quantity']:
            raise serializers.ValidationError({'quantity': ['Product has no stock']})

        return data


class CouponSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ('code', 'type', 'discount')

    
    def get_type(self, obj):
        return obj.get_type()


class OrderSerializer(FlexFieldsModelSerializer):
    status = serializers.SerializerMethodField()
    payment = PaymentSerializer(required=True)
    products = OrderProductSerializer(many=True, required=False)
    coupon = serializers.PrimaryKeyRelatedField(queryset=Coupon.objects.all(), required=False)

    class Meta:
        model = Order
        fields = ['id', 'user', 'created', 'payment', 'status', 'products', 'coupon']
        read_only_fields = ['id', 'created']
    

    def get_status(self, obj):
        return obj.get_status()

    
    def create(self, validated_data):
        # pop nested data
        products_data = validated_data.pop('products', None)
        payment_data = validated_data.pop('payment')

        # create payment
        payment = Payment.objects.create(**payment_data)

        #create order
        order = Order.objects.create(payment=payment, **validated_data)

        if not products_data == None:
            for product in products_data:
                # pop order, since it will be passed automatically
                product.pop('order', None)

                # pop id, since it should fallback to default
                product.pop('id', None)

                # create OrderProduct
                OrderProduct.objects.create(order=order, **product) 

        
        return order


    def update(self, instance, validated_data):
        # get nested data
        order_products = validated_data.pop('products', [])
        payment_data = validated_data.pop('payment')

        # payment instance
        payment = instance.payment

        # updating order
        instance.user = validated_data.get('user', instance.user)
        instance.status = validated_data.get('status', instance.status)
        instance.coupon = validated_data.get('coupon', instance.coupon)
        instance.save()

        # updating payment
        payment.amount = payment_data.get('amount', payment_data['amount'])
        payment.save()

        # get all OrderProducts that belongs to this order
        order_products_with_order_id = OrderProduct.objects.filter(order=instance.pk).values_list('id', flat=True)
        order_products_id_pool = []

        # iterate through found OrderProducts
        for order_product in order_products:
            # check if OrderProduct has an id
            if "id" in order_product.keys():
                # if so, update id
                try:
                    # to get an OrderProduct's instance, the id shoud be an UUID
                    order_product_instance = OrderProduct.objects.get(id=uuid.UUID(order_product['id']))
                    order_product_instance.product = order_product.get('product', order_product_instance.product)
                    order_product_instance.quantity = order_product.get('quantity',order_product_instance.quantity)
                    order_product_instance.save()

                    # the accessable id is not an UUID
                    # so converts the OrderProduct id to UUID before appending it to the new OrderProduct's pool
                    order_products_id_pool.append(uuid.UUID(order_product_instance.pk))
                except:
                    continue
            else:
                # if not, create a new one

                # pop order, since it will be passed automatically
                order_product.pop('order', None)

                # pop id, since it should fallback to default
                order_product.pop('id', None)

                order_product_instance = OrderProduct.objects.create(order=instance, **order_product)

                # id returned from Model.objects.create() is already an UUID
                order_products_id_pool.append(order_product_instance.pk)
        
        for order_product_id in order_products_with_order_id:
            # again, the id returned from Model.objects.filter() is not UUID, so it needs to be converted
            if uuid.UUID(order_product_id) not in order_products_id_pool:
                # if OrderProducts in the request was not updated neither created, delete it
                OrderProduct.objects.filter(pk=order_product_id).delete()

        return instance