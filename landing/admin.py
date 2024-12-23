from django.contrib import admin

# Register your models here.
from .models import SocialLink, LandingPageContent, FooterColumn, FooterLink
from unfold.admin import ModelAdmin

@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ('platform', 'url', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('platform', 'url')

@admin.register(LandingPageContent) 
class LandingPageContentAdmin(ModelAdmin):
    list_display = ('header_title', 'created_at', 'updated_at')
    search_fields = ('header_title', 'header_description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(FooterColumn)
class FooterColumnAdmin(ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('links',)

@admin.register(FooterLink)
class FooterLinkAdmin(ModelAdmin):...