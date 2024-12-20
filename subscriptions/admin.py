from django.contrib import admin
from .models import Package,PackageToken,SubscriptionPlan, SubscriptionPlanDuration
from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms
from django.db.models import Count
from platforms.models import Account

class AccountInline(TabularInline):
    model = Account
    extra = 1  # Số lượng tài khoản mặc định khi tạo mới (có thể điều chỉnh)
    fields = ['platform', 'name', 'is_active', 'rented_by', 'expires_at']  # Các trường bạn muốn hiển thị trong bảng

    # Nếu bạn muốn tự động thêm người dùng vào tài khoản khi tạo, bạn có thể thêm hàm save_formset (không bắt buộc)
    def save_formset(self, request, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            # Gán thêm người dùng vào tài khoản nếu chưa có
            if not instance.rented_by:
                instance.rented_by = request.user  # Giả sử bạn muốn người dùng đang đăng nhập làm chủ tài khoản
            instance.save()
        formset.save_m2m()
class PackageTokenAdminForm(forms.ModelForm):
    class Meta:
        model = PackageToken
        fields = '__all__'
    # Override phương thức để thay đổi queryset của trường 'package'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['package'].queryset = Package.objects.annotate(
            buyers_count=Count('buyers')
        ).filter(buyers_count__lt=models.F('max_users'))
        
# Register your models here.
@admin.register(Package)
class PackageAdmin(ModelAdmin):
    autocomplete_fields = ['buyers',]
    list_display = ('name','subscription_plan__name','max_users','get_buyers_count')
    def get_buyers_count(self, obj):
            # Trả về số lượng người mua trong gói
        return obj.buyers.count()
    get_buyers_count.short_description = 'Số lượng người dùng'
@admin.register(PackageToken)
class PackageTokenAdmin(ModelAdmin):
    # Override phương thức get_queryset để chỉ lấy các gói khả dụng
    form = PackageTokenAdminForm
    list_display = ('package', 'token', 'user', 'expires_at', 'is_active')
    
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelAdmin):
    list_display = ('name', 'description', 'level')
    list_filter = ('level',)
    search_fields = ('name', 'description')
    filter_horizontal = ('platforms',)

@admin.register(SubscriptionPlanDuration)
class SubscriptionPlanDurationAdmin(ModelAdmin):
    list_display = ('subscription_plan', 'duration', 'price_display', 'pre_price_display', 'price_per_month', 'discount_percentage')
    list_filter = ('subscription_plan',)
    search_fields = ('subscription_plan__name',)

    def price_display(self, obj):
        return f"{int(obj.price):,} VND"
    price_display.short_description = "Giá hiện tại"

    def pre_price_display(self, obj):
        if obj.pre_price:
            return f"{int(obj.pre_price):,} VND"
        return "-"
    pre_price_display.short_description = "Giá gốc"

    def price_per_month(self, obj):
        return f"{int(obj.price_per_month()):,} VND"
    price_per_month.short_description = "Giá mỗi tháng"

    def discount_percentage(self, obj):
        return obj.discount_percentage
    discount_percentage.short_description = "Khuyến mãi"