from .models import Payment
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PaymentSerializer
from django_filters import rest_framework as filters


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_fields = ['is_paid', 'type']