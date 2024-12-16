from django.contrib import admin

# Register your models here.
from .models import SocialLink, LandingPageContent
from unfold.admin import ModelAdmin

@admin.register(SocialLink)
class SocialLinkAdmin(ModelAdmin):
    list_display = ('platform', 'url', 'icon', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('platform', 'url')

@admin.register(LandingPageContent) 
class LandingPageContentAdmin(ModelAdmin):
    list_display = ('header_title', 'created_at', 'updated_at')
    search_fields = ('header_title', 'header_description')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('social_links',)
