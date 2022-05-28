import decimal
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError
from django.db.models import Sum
from .models import CashRegister, Payment, Transaction


def field_bigger_than_0(value):
        if value <= 0:
            raise serializers.ValidationError('Value should be bigger than 0')


def integer_field(value):
    if value < 0:
        raise serializers.ValidationError('Value should be bigger or equal to 0')


class PaymentSerializer(serializers.ModelSerializer):
    paid_amount = serializers.SerializerMethodField()


    class Meta:
        model = Payment
        fields = ('id', 'amount', 'is_paid', 'created', 'paid_amount', 'type')
        read_only_fields = ['id', 'created']
        extra_kwargs = {
            'amount': { 'validators': [field_bigger_than_0] }
        }


    def get_paid_amount(self, obj):
        paid = Transaction.objects.filter(payment=obj.id).aggregate(Sum('amount'))

        return str(paid['amount__sum'] if paid['amount__sum'] else decimal.Decimal())


class CashRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = CashRegister
        fields = '__all__'
        read_only_fields = ['id', 'created', 'updated']
        extra_kwargs = {
            'initial_amount': { 'validators': [integer_field] },
            'closed_amount': { 'validators': [integer_field] },
            'open': { 'validators': [validators.UniqueValidator(queryset=CashRegister.objects.filter(open=True))] }
        }


class TransactionSerializer(serializers.ModelSerializer):
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all())

    class Meta:
        model = Transaction
        fields = ('id', 'payment', 'cash_register', 'amount', 'created', 'type', 'details')
        read_only_fields = ['id', 'created']
        extra_kwargs = {
            'amount': { 'validators': [field_bigger_than_0] }
        }