from django.contrib import admin
from .models import PackageToken,SubscriptionPlan, SubscriptionPlanDuration, SubscriptionDurationFilter
from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from django.utils.translation import gettext_lazy as _
from django.db import models
from django import forms
from django.db.models import Count
from platforms.models import Account,AccountGroup

from unfold.contrib.import_export.forms import ExportForm, ImportForm
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget



@admin.register(SubscriptionDurationFilter)
class SubscriptionDurationFilterAdmin(ModelAdmin,ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm

class AccountInline(TabularInline):
    model = Account
    extra = 1  # Số lượng tài khoản mặc định khi tạo mới (có thể điều chỉnh)
    fields = ['platform', 'name', 'is_active', 'rented_by', 'expires_at']  # Các trường bạn muốn hiển thị trong bảng
    import_form_class = ImportForm
    export_form_class = ExportForm
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
        self.fields['account_group'].queryset = AccountGroup.objects.annotate(
            buyers_count=Count('buyers')
        ).filter(buyers_count__lt=models.F('max_users'))
        

@admin.register(PackageToken)
class PackageTokenAdmin(ModelAdmin,ImportExportModelAdmin):
    # Override phương thức get_queryset để chỉ lấy các gói khả dụng
    form = PackageTokenAdminForm
    list_display = ('account_group', 'token', 'user', 'expires_at', 'is_active')
    import_form_class = ImportForm
    
@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('name', 'description', 'level')
    list_filter = ('level',)
    search_fields = ('name', 'description')
    filter_horizontal = ('platforms',)
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }
    
@admin.register(SubscriptionPlanDuration)
class SubscriptionPlanDurationAdmin(ModelAdmin,ImportExportModelAdmin):
    list_display = ('subscription_plan', 'duration', 'price_display', 'pre_price_display', 'price_per_month', 'discount_percentage')
    list_filter = ('subscription_plan',)
    search_fields = ('subscription_plan__name',)
    import_form_class = ImportForm
    export_form_class = ExportForm
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