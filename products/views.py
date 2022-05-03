from .models import Product, Supplier
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import ProductSerializer, SupplierSerializer
from rest_framework.filters import SearchFilter
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter


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
    search_fields = ['name']
    ordering_fields = ['name', 'created', 'price']
    ordering = ['name']


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['name', 'email', 'phone', 'city', 'cnpj']
    ordering = ['name']