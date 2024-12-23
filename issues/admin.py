# admin.py

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Issue

@admin.register(Issue)
class IssueAdmin(ModelAdmin):
    list_display = ('user', 'content','status', 'image', 'created_at', 'updated_at')