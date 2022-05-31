from django.contrib import admin
from payments.models import CashRegister, Payment, Transaction


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('created', 'amount', 'is_paid', 'type')
    list_filter = ('created', 'type', 'is_paid')


class CashRegisterAdmin(admin.ModelAdmin):
    list_display = ('created', 'details', 'initial_amount', 'user')
    list_filter = ['created', 'user']
    search_fields = ['details']


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('created', 'details', 'amount', 'type')
    list_filter = ['created', 'cash_register', 'payment']

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(CashRegister, CashRegisterAdmin)