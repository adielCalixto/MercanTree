from .models import Product, Supplier
from rest_framework import viewsets, permissions, status
from .serializers import ProductSerializer, SupplierSerializer
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist
from orders.models import OrderProduct


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'barcode']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, filters.DjangoFilterBackend, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'barcode']
    ordering_fields = ['name', 'created', 'price']
    ordering = ['name']

    @action(detail=True, methods=['get'])
    def in_stock_count(self, request, pk=None):
        try:
            product = Product.objects.get(id=pk)
        except ObjectDoesNotExist:
            return Response({'detail': 'Not found.'},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(product)
        product_count = serializer.data['quantity']

        in_order_count = OrderProduct.objects.filter(product_id=pk).aggregate(Sum('quantity'))
        count = product_count - (in_order_count['quantity__sum'] if in_order_count['quantity__sum'] else 0)

        return Response({'count': count},
                        status.HTTP_200_OK)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone', 'city', 'cnpj']
    ordering = ['name']