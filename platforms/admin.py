from django.contrib import admin
from .models import Platform, Account, AccountCookie,AccountGroup
from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from django.utils.translation import gettext_lazy as _
from django.db import models
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm
from django.utils.timezone import timezone,now
# Register your models here.
@admin.register(Platform)
class PlatformAdmin(ModelAdmin,ImportExportModelAdmin):
    radio_fields = {"login_choice": admin.VERTICAL}
    list_display = [
        "name",
        "login_choice",
        "url",
        "created_at",
    ]
    search_fields = ["name",'login_choice','description']
    list_filter = ["login_choice"]
    import_form_class = ImportForm
    export_form_class = ExportForm
    
class AccountCookieInline(TabularInline):
    model = AccountCookie
    extra = 1
    
@admin.register(AccountGroup)
class AccountGroupAdmin(ModelAdmin,ImportExportModelAdmin):
    autocomplete_fields = ['buyers',]
    list_display = ('name','subscription_duration','max_users','get_buyers_count','get_accounts_count')
    import_form_class = ImportForm
    export_form_class = ExportForm
    filter_horizontal = ['accounts']
    def get_buyers_count(self, obj):
        return obj.buyers.count()
    def get_accounts_count(self, obj):
        return obj.accounts.count()
    get_accounts_count.short_description = 'Số lượng tài khoản'
    get_buyers_count.short_description = 'Số lượng người dùng'
    
@admin.register(Account)
class PlatformAccountAdmin(ModelAdmin,ImportExportModelAdmin): 
    inlines = [AccountCookieInline,]
    autocomplete_fields = ['rented_by']
    list_display = [
        "name",
        "platform__name",
        "rented_by",
        "username",
        "is_active",
        "total_users",
        "days_remaining"
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    ("platform","name"),
                    ("username","password"),
                    "two_factor_auth",
                    "rented_by",
                    "rented_at",
                    "expires_at",
                    "buy_date",
                    "expiry_date",
                    "is_active"
                )
            },
        ),
    )
    search_fields = [
        "name",
        "platform__name",
    ]
    import_form_class = ImportForm
    export_form_class = ExportForm
    def days_remaining(self,cls):
        if cls.expiry_date:
            # Lấy thời gian hiện tại
            current_time = now()
            # Tính toán số ngày còn lại từ thời điểm hiện tại đến expiry_date
            delta = cls.expiry_date - current_time
            return f"Còn {max(delta.days, 0)} ngày"  # Đảm bảo không trả về giá trị âm
        return None
    days_remaining.short_description = 'Hạn sử dụng (Admin)'
    
    def total_users(self, obj):
        """
        Tính tổng số người đang sử dụng tài khoản này thông qua các AccountGroup liên kết.
        """
        return obj.accounts.aggregate(total=models.Count('buyers', distinct=True))['total'] or 0
    total_users.short_description = 'Số người dùng'