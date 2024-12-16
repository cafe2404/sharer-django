from django.contrib import admin
from .models import Platform, Account, AccountCookie
from django.contrib import admin
from unfold.admin import ModelAdmin,TabularInline
from django.utils.translation import gettext_lazy as _
from unfold.contrib.forms.widgets import WysiwygWidget,ArrayWidget
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Register your models here.
@admin.register(Platform)
class PlatformAdmin(ModelAdmin):
   ...
class AccountCookieInline(TabularInline):
    model = AccountCookie
    extra = 1
    
    
@admin.register(Account)
class PlatformAccountAdmin(ModelAdmin): 
    inlines = [AccountCookieInline,]
    autocomplete_fields = ['rented_by']
    list_display = [
        "platform__name",
        "name",
        "expires_at",
    ]
    search_fields = [
        "name",
        "platform__name",
    ]
