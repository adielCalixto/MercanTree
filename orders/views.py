from rest_framework import viewsets
from rest_framework import permissions
from .models import Order, OrderProduct
from .serializers import OrderSerializer, OrderProductSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter


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


class OrderProductViewSet(viewsets.ModelViewSet):
    queryset = OrderProduct.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderProductSerializer
    ordering = ['quantity']