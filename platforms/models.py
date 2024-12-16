from django.db import models
from custom_user.models import CustomUser as User
from django.utils.timezone import now
from datetime import timedelta

# Create your models here.
class Platform(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    logo_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Nền tảng'
        verbose_name_plural = 'Nền tảng'
class Account(models.Model):
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)  # Trạng thái của tài khoản
    rented_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="rented_accounts")
    rented_at = models.DateTimeField(null=True, blank=True)  # Thời điểm bắt đầu thuê
    expires_at = models.DateTimeField(null=True, blank=True)  # Thời điểm hết hạn thuê
    package = models.ForeignKey('subscriptions.Package', on_delete=models.CASCADE, related_name="accounts",null=True,blank=True)  # Chỉnh sửa mối quan hệ ForeignKey
    def __str__(self):
        return f"{self.platform.name} - {self.name}"
    class Meta:
        verbose_name = 'Tài khoản'
        verbose_name_plural = 'Tài khoản'
    def is_expired(self):
        return self.expires_at and now() > self.expires_at
    def rent(self, user, duration_days):
        if self.rented_by is not None and not self.is_expired():
            raise ValueError(f"Account {self.username} is currently rented by another user.")
        self.rented_by = user
        self.rented_at = now()
        self.expires_at = self.rented_at + timedelta(days=duration_days)
        self.is_active = False 
        self.save()
    def release(self):
        if self.is_expired():
            self.rented_by = None
            self.rented_at = None
            self.expires_at = None
            self.is_active = True  
            self.save()
   
class AccountCookie(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    cookie = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.account.platform.name}-{self.account.name} Cookie"
    class Meta:
        verbose_name = 'Cookie'
        verbose_name_plural = 'Cookie'