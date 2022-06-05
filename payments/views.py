import decimal
from .models import Payment, Transaction, CashRegister
from rest_framework import viewsets
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CashRegisterSerializer, PaymentSerializer, TransactionSerializer
from django_filters import rest_framework as filters
from django.db.models import Sum
from rest_framework.filters import OrderingFilter
from django.db.models.signals import post_save
from django.dispatch import receiver

class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_paid']
    ordering = ['-created']


    @action(methods=['post'], detail=True)
    def deposit(self, request, pk=None):
        serializer = TransactionSerializer(data={**request.data, 'payment': pk, 'type': 'CI'})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=True)
    def withdraw(self, request, pk=None):
        serializer = TransactionSerializer(data={**request.data, 'payment': pk, 'type': 'CB'})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CashRegister(viewsets.ModelViewSet):
    queryset = CashRegister.objects.all()
    serializer_class = CashRegisterSerializer
    permission_classes = [permissions.IsAdminUser|permissions.IsAuthenticated & ReadOnly]
    filter_backends = [filters.DjangoFilterBackend, OrderingFilter]
    ordering = ['-created']
    filterset_fields = ['open']

    @action(methods=['get'], detail=True)
    def transactions(self, request, pk=None):
        transactions = Transaction.objects.filter(cash_register=pk).order_by('-created')
        page = self.paginate_queryset(transactions)

        if page is not None:
            serializer = TransactionSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    
    @action(methods=['get'], detail=True)
    def report(self, request, pk=None):
        cash_register = self.get_object()

        transaction_deposit = Transaction.objects.filter(cash_register=pk, type='CI').aggregate(Sum('amount'))
        transaction_withdraw = Transaction.objects.filter(cash_register=pk, type='CB').aggregate(Sum('amount'))
        
        initial_amount = cash_register.initial_amount
        final_amount = initial_amount - (transaction_withdraw['amount__sum'] or 0) + (transaction_deposit['amount__sum'] or 0)

        return Response({
            'initial_amount': str(initial_amount),
            'final_amount': str(final_amount)
        },
        status=status.HTTP_200_OK)


@receiver(post_save, sender=Transaction)
def check_is_paid(sender, instance=None, created=False, **kwargs):
    # logic to cash_deposit payments
    if created and instance.type == 'CI':
        # get payment serializer to access paid_amount
        serializer = PaymentSerializer(instance=instance.payment)

        # if paid_amount is equal to or bigger than the payment amount, set it as paid
        if decimal.Decimal(serializer.data.get('amount')) <= decimal.Decimal(serializer.data.get('paid_amount')):
            serializer = PaymentSerializer(instance=instance.payment, data={'is_paid': True}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()