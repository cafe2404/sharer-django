from django.contrib import admin
from .models import Platform, PlatformAccount, AccountGroup
from unfold.admin import ModelAdmin
from unfold.decorators import  display
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(Platform)
class PlatformAdmin(ModelAdmin):
    ...
@admin.register(PlatformAccount)
class PlatformAccountAdmin(ModelAdmin): 
    autocomplete_fields = ['users']
    list_display = [
        "platform__name",
        "username",
        "expired_at",
        "login",
    ]
    search_fields = [
        "username",
        "platform__name",
    ]
@admin.register(AccountGroup)
class AccountGroupAdmin(ModelAdmin):
    autocomplete_fields = ['users']