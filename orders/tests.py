from django.test import TestCase
from django.utils import timezone
from .serializers import OrderSerializer, OrderProductSerializer
from .models import Order, OrderProduct
from products.models import Product
from payments.models import Payment
from users.models import User


class OrderModelTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='a',
        description='a',
        barcode='a',
        expires_at=timezone.now(),
        price=1,
        category='a')

        self.payment = Payment.objects.create(is_paid=False)

        self.user = User.objects.create_user(username='a',
        email='a',
        password='a')

    def test_order_created(self):
        order = OrderSerializer(data={'value': 1,
        'user_id': self.user.id,
        'payment_id': self.payment.id})
        order.is_valid(raise_exception=True)
        order.save()

        order2 = OrderSerializer(data={'value': 1,
        'user_id': self.user.id,
        'payment_id': self.payment.id,
        'products': [{'quantity': 1, 'product_id': self.product.id}]})
        order2.is_valid(raise_exception=True)
        order2.save()

        self.assertTrue(Order.objects.count() > 1)
        self.assertTrue(OrderProduct.objects.count() > 0)

    def test_order_updated(self):
        order = OrderSerializer(data={'value': 100,
        'user_id': 1,
        'payment_id': 1})
        order.is_valid(raise_exception=True)
        order.save()

        new_order = OrderSerializer(instance=order.instance, data={'value': 200,
        'user_id': 1,
        'payment_id': 1,
        'products': []})
        new_order.is_valid(raise_exception=True)
        new_order.save()

        order = Order.objects.get(id=order.data.get('id'))

        self.assertEqual(order.value, new_order.validated_data.get('value'))
        self.assertEqual(order.user_id, new_order.validated_data.get('user_id'))
        self.assertEqual(order.payment_id, new_order.validated_data.get('payment_id'))

    def test_order_destroyed(self):
        order = OrderSerializer(data={'value': 100, 'user_id': 1, 'payment_id': 1})
        order.is_valid(raise_exception=True)
        order.save()

        count = Order.objects.count()
        o = Order.objects.get(id=order.data.get('id'))
        o.delete()
        new_count = Order.objects.count()

        self.assertTrue(count > new_count)