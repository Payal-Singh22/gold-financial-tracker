from django.contrib import admin
from .models import Customer, Bill, BillItem, OldGold, Payment, GoldRate, SilverRate, BarRate


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'created_at']
    search_fields = ['name', 'phone', 'email']
    list_filter = ['created_at']


@admin.register(GoldRate)
class GoldRateAdmin(admin.ModelAdmin):
    list_display = ['rate_24k', 'updated_by', 'updated_at', 'is_active']
    list_filter = ['is_active', 'updated_at']


@admin.register(SilverRate)
class SilverRateAdmin(admin.ModelAdmin):
    list_display = ['rate_per_gram', 'updated_by', 'updated_at', 'is_active']
    list_filter = ['is_active', 'updated_at']


@admin.register(BarRate)
class BarRateAdmin(admin.ModelAdmin):
    list_display = ['rate_per_gram', 'updated_by', 'updated_at', 'is_active']
    list_filter = ['is_active', 'updated_at']


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ['bill_number', 'customer', 'bill_date', 'net_payable', 'status', 'created_by']
    list_filter = ['status', 'bill_date', 'created_by']
    search_fields = ['bill_number', 'customer__name']
    readonly_fields = ['bill_number', 'created_at', 'updated_at']


@admin.register(BillItem)
class BillItemAdmin(admin.ModelAdmin):
    list_display = ['bill', 'item_type', 'material_type', 'description', 'net_weight', 'tunch_wstg', 'g_fine', 'amount']
    list_filter = ['bill__bill_date', 'item_type', 'material_type']


@admin.register(OldGold)
class OldGoldAdmin(admin.ModelAdmin):
    list_display = ['bill', 'weight', 'rate_per_gram', 'value', 'created_at']
    list_filter = ['created_at']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['bill', 'amount', 'payment_method', 'payment_date', 'created_by']
    list_filter = ['payment_method', 'payment_date']
    search_fields = ['bill__bill_number']

