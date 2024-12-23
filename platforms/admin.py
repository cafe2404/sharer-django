from django.contrib import admin
from .models import Platform, Account, AccountCookie,AccountGroup
from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from unfold.contrib.forms.widgets import WysiwygWidget
from django.db import models
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

# Register your models here.
@admin.register(Platform)
class PlatformAdmin(ModelAdmin,ImportExportModelAdmin):
    formfield_overrides = {
        models.TextField: {
            "widget": WysiwygWidget,
        },
    }
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
class PackageAdmin(ModelAdmin,ImportExportModelAdmin):
    autocomplete_fields = ['buyers',]
    list_display = ('name','subscription_duration','max_users','get_buyers_count')
    import_form_class = ImportForm
    export_form_class = ExportForm
    def get_buyers_count(self, obj):
        return obj.buyers.count()
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
        "expires_at",
        "expiry_date_admin"
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
                    "is_active",
                    "expiry_date",
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
    def expiry_date_admin(self, obj):
        now = datetime.now()
        if obj.expiry_date:
            expiry_date = now + timedelta(days=obj.expiry_date)
            days_remaining = (expiry_date - now).days
            return f"Còn lại {days_remaining} ngày"
        else:
            return None
        return None  # Nếu đã hết hạn hoặc không có ngày hết hạn
    expiry_date_admin.short_description = 'Hạn sử dụng (Admin)'
    