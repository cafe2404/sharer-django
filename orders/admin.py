from django.contrib import admin
from .models import Order, PaymentSetting
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

# Register your models here.
@admin.register(Order)
class OrderAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('order_id', 'user', 'subscription_plan','subscription_duration','amount', 'status', 'is_used', 'created_at', 'updated_at')
    list_filter = ('status', 'is_used', 'created_at')
    search_fields = ('order_id', 'user__username', 'subscription_plan__name')
    readonly_fields = ('order_id', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    import_form_class = ImportForm
    export_form_class = ExportForm
    
@admin.register(PaymentSetting)
class PaymentSettingAdmin(ModelAdmin):
    list_display = ('payment_method', 'account_number', 'bank_code','is_active', 'created_at', 'updated_at')