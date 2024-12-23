# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from custom_user.models import CustomUser as User 
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.decorators import  display


@admin.register(User)
class CustomAdminClass(BaseUserAdmin,ModelAdmin): 
    list_display = [
        "display_header",
        "is_active",
        "display_staff",
        "display_superuser",
    ]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Thông tin cá nhân"),
            {
                "fields": (("first_name", "last_name"),( "email","phone_number"), "avatar"),
                "classes": ["tab"],
            },
        ),
        (
            _("Quyền truy cập"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ["tab"],
            },
        ),
        (
            _("Ngày quan trọng"),
            {
                "fields": ("last_login", "date_joined"),
                "classes": ["tab"],
            },
        ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
    )
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_filter = ("is_staff",)
    @display(description=_("User"))
    def display_header(self, instance: User):
        return instance.username

    @display(description=_("Staff"), boolean=True)
    def display_staff(self, instance: User):
        return instance.is_staff

    @display(description=_("Superuser"), boolean=True)
    def display_superuser(self, instance: User):
        return instance.is_superuser

