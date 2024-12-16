from django.contrib import admin
from .models import Coupon
from unfold.admin import ModelAdmin
@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ('code', 'discount_amount',"usage_limit","times_used" ,'additional_days', 'expiration_date', 'is_active')
    search_fields = ('code',)
    list_filter = ('is_active',)
