import decimal
from rest_framework import serializers
from django.db.models import Sum
from .models import Payment, PaymentCharge


class PaymentSerializer(serializers.ModelSerializer):
    paid_amount = serializers.SerializerMethodField()


    class Meta:
        model = Payment
        fields = ('id', 'amount', 'is_paid', 'created', 'paid_amount')
        read_only_fields = ['id', 'created']


    def get_paid_amount(self, obj):
        paid = PaymentCharge.objects.filter(payment=obj.id).aggregate(Sum('charge'))

        return paid['charge__sum'] if paid['charge__sum'] else decimal.Decimal('0.00')


class PaymentChargeSerializer(serializers.ModelSerializer):
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all())

    class Meta:
        model = PaymentCharge
        fields = ('id', 'payment', 'charge', 'created', 'type')
        read_only_fields = ['id', 'created']
