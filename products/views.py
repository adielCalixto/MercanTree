from django.utils import timezone
from .models import Category, Product, Supplier
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer, SupplierSerializer
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.db.models import Sum, F


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
        end_date = timezone.now()
        start_date = end_date - timezone.timedelta(days=6)
        products = Product.objects.filter(expires_at__range=[start_date, end_date]).order_by('-expires_at')
        
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    
    @action(methods=['GET'], detail=False)
    def paid_price(self, request):
        product_paid_amount = Product.objects.aggregate(total=Sum(F('supplier_price')*F('quantity')))['total']

        return Response({
            'amount': '%.2f' % product_paid_amount if product_paid_amount else 0,
        })


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