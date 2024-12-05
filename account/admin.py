# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from account.models import CustomUser
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import  display


@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    search_fields = [
        'username'
    ]
    list_display = [
        
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
    ]
    change_password_form = AdminPasswordChangeForm
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Avatar', {'fields': ('avatar',)}),
    )
    
    @display(description=_("User"))
    def display_header(self, instance: CustomUser):
        return instance.username
    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: CustomUser):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: CustomUser):
        return instance.is_superuser

