from django.utils import timezone
from rest_framework import viewsets
from rest_framework import permissions
from django.db.models import Sum
from payments.models import Payment
from .models import Order, OrderProduct, Coupon
from .serializers import OrderSerializer, OrderProductSerializer, CouponSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response


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
    ordering_fields = ['created', 'payment__is_paid']
    ordering = ['-created']

    @action(methods=['GET'], detail=False)
    def payment_amount(self, request):
        interval = request.query_params.get('interval')
        interval_list = { 'month': 30, 'week': 6, 'day': 1 }

        days = interval_list.get(interval, 30)

        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=days)
        payment_amount = Payment.objects.filter(created__range=[start_date, end_date], type='SALE').aggregate(Sum('amount'))
        amount = payment_amount['amount__sum'] if payment_amount['amount__sum'] else 0

        return Response({'amount': '%.2f' % amount})


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderProductSerializer
    ordering = ['reference']
    filter_backends = [OrderingFilter]


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CouponSerializer
    ordering = ['code']
    filter_backends = [OrderingFilter]