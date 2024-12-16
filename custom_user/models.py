# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from datetime import timedelta
from subscriptions.models import PackageToken
def generate_random_token(length=64):
    return get_random_string(length=length)

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username
    def get_current_package(self):
        """Lấy gói đăng ký hiện tại của người dùng từ PackageToken"""
        token = PackageToken.objects.filter(user=self, is_active=True).first()
        return token.package if token else None

class UserToken(models.Model):
    token = models.CharField(max_length=64, unique=True, default=generate_random_token)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='user_token')  # Một người dùng chỉ có một UserToken
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            # UserToken mặc định có thời hạn 1 năm
            self.expires_at = now() + timedelta(days=365)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"UserToken for {self.user.username}"

    def is_expired(self):
        """Kiểm tra token đã hết hạn chưa."""
        return now() > self.expires_at

    def renew(self, duration_days=365):
        """Gia hạn UserToken."""
        self.expires_at = now() + timedelta(days=duration_days)
        self.save()
