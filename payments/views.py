import decimal
from .models import Payment, PaymentCharge
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PaymentSerializer, PaymentChargeSerializer
from django_filters import rest_framework as filters
from rest_framework.filters import OrderingFilter
from django.db.models.signals import post_save
from django.dispatch import receiver


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_paid']
    ordering = ['-created']

    @action(methods=['post'], detail=True)
    def charge_amount(self, request, pk=None):
        serializer = PaymentChargeSerializer(data={**request.data, 'payment': pk, 'type': 'CD'})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@receiver(post_save, sender=PaymentCharge)
def check_is_paid(sender, instance=None, created=False, **kwargs):
    # logic to cash_deposit payments
    if created and instance.type == 'CD':
        # get payment serializer to access paid_amount
        serializer = PaymentSerializer(instance=instance.payment)

        # if paid_amount is equal to or bigger than the payment amount, set it as pais
        if decimal.Decimal(serializer.data.get('amount')) <= decimal.Decimal(serializer.data.get('paid_amount')):
            serializer = PaymentSerializer(instance=instance.payment, data={'is_paid': True}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()