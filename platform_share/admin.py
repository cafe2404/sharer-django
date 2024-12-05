from django.contrib import admin
from .models import Platform, PlatformAccount
from unfold.admin import ModelAdmin

# Register your models here.
@admin.register(Platform)
class PlatformAdmin(ModelAdmin):
    ...
@admin.register(PlatformAccount)
class PlatformAccountAdmin(ModelAdmin): 
    ...