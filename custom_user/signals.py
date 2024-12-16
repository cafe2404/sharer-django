from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserToken
from datetime import timedelta
from django.utils.timezone import now
from .models import CustomUser as User

@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        # Tạo UserToken sau khi tài khoản được tạo
        UserToken.objects.create(
            user=instance,
            expires_at=now() + timedelta(days=365)  # Thời hạn mặc định là 1 năm
        )
