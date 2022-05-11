from rest_framework import viewsets, status
from rest_framework import permissions
from .models import Order, OrderProduct, Coupon
from .serializers import OrderSerializer, OrderProductSerializer, CouponSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from payments.models import Payment
from payments.serializers import PaymentSerializer
from django.core.exceptions import ObjectDoesNotExist


class OrderFilter(filters.FilterSet):
    min_value = filters.NumberFilter(field_name="value", lookup_expr='gte')
    max_value = filters.NumberFilter(field_name="value", lookup_expr='lte')

    class Meta:
        model = Order
        fields = []
        

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ['created', 'price']
    ordering = ['-created']

    @action(methods=['get'], detail='true')
    def products(self, request, pk=None):
        products = OrderProduct.objects.filter(order=pk)
        page = self.paginate_queryset(products)

        if page is not None:
            serializer = OrderProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderProductSerializer(products, many=True)
        return Response(serializer.data)


    @action(methods=['get'], detail='true')
    def payment(self, request, pk=None):
        order = self.get_object()
        payment = Payment.objects.get(id=order.payment.id)

        serializer = PaymentSerializer(payment)
        return Response(serializer.data)
        

    @action(methods=['get'], detail='true')
    def coupon(self, request, pk=None):
        order = self.get_object()
        if order.coupon is None:
            return Response({'details': 'Order has no coupon'},
            status=status.HTTP_400_BAD_REQUEST)
        coupon = Coupon.objects.get(code=order.coupon.code)

        serializer = CouponSerializer(coupon)
        return Response(serializer.data)


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderProductSerializer
    ordering = ['quantity']
    filter_backends = [OrderingFilter]


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CouponSerializer
    ordering = ['code']
    filter_backends = [OrderingFilter]