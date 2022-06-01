from datetime import date, timedelta
from .models import Category, Product, Supplier
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
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
    search_fields = ['name', 'barcode']
    ordering_fields = ['name', 'created', 'price', 'expires_at']
    ordering = ['expires_at', 'name']


    @action(methods=['GET'], detail=False)
    def next_to_expiration(self, request):
        start_date = date.today()
        end_date = start_date + timedelta(days=6)
        products = Product.objects.filter(expires_at__range=[start_date, end_date])
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email', 'phone', 'city', 'cnpj']
    ordering = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering = ['name']