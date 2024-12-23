from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import PackageToken

# Tín hiệu xóa người dùng khỏi danh sách buyers khi token bị xóa
@receiver(post_delete, sender=PackageToken)
def remove_user_from_package_buyers(sender, instance, **kwargs):
    # Xóa người dùng khỏi danh sách buyers của package khi token bị xóa
    if instance.user and instance.account_group:
        instance.account_group.buyers.remove(instance.user)
        instance.account_group.save()