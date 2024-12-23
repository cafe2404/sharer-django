from django.db import models
from django.utils.timezone import now
from datetime import timedelta,datetime


# Create your models here.
class Platform(models.Model):
    class LoginChoice(models.TextChoices):
        cookie = 'cookie', 'Cookie'
        rankerfox = 'rankerfox', 'Rankerfox'
        adspower = 'adspower', 'Ads Power'
        spy = 'spy', 'Spy Essentials'
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500,verbose_name='Mô tả ngắn (Tối đa 500 từ)')
    login_choice = models.CharField(
        max_length=255, 
        choices=LoginChoice.choices, 
        default=LoginChoice.cookie,
        null=True,blank=True,
        verbose_name='Phương thức đăng nhập'
    )
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
    username = models.CharField(max_length=255,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    two_factor_auth = models.CharField(max_length=255,null=True,blank=True)
    rented_by = models.ForeignKey('custom_user.CustomUser', null=True, blank=True, on_delete=models.SET_NULL, related_name="rented_accounts",verbose_name="Người mua")
    rented_at = models.DateTimeField(null=True, blank=True, verbose_name='Thời gian mua (user)')  # Thời điểm bắt đầu thuê
    expires_at = models.DateTimeField(null=True, blank=True,verbose_name='Thời gian hết hạn (user)')  # Thời điểm hết hạn thuê
    buy_date = models.DateTimeField(null=True, blank=True, verbose_name='Thời gian mua (admin)')  # Thời điểm bắt đầu thuê
    expiry_date = models.DateTimeField(null=True, blank=True,verbose_name='Thời gian hết hạn (admin)')  # Thời điểm hết hạn thuê
    is_active = models.BooleanField(default=True, verbose_name='Hoạt động')  # Trạng thái của tài khoản
    
    
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
 # Nếu đã hết hạn hoặc không có ngày hết hạn 
    
class AccountCookie(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    cookie = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.account.platform.name}-{self.account.name} Cookie"
    class Meta:
        verbose_name = 'Cookie'
        verbose_name_plural = 'Cookie'
        
# Gói đăng ký bán cho người dùng (Package)
class AccountGroup(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    subscription_duration = models.ForeignKey(
        'subscriptions.SubscriptionPlanDuration', on_delete=models.SET_NULL, related_name='account_groups',null=True
    )
    max_users = models.PositiveIntegerField(default=10,verbose_name='Giới hạn người dùng')  # Giới hạn số người dùng
    buyers = models.ManyToManyField('custom_user.CustomUser', related_name='bought_packages',blank=True)
    accounts = models.ManyToManyField(Account, related_name='accounts', blank=True, verbose_name="Tài khoản trong nhóm")
    class Meta:
        verbose_name = "Nhóm tài khoản"
        verbose_name_plural = "Nhóm tài khoản"
        ordering = ['-id']
    def __str__(self):
        return f"{self.name}-{self.subscription_duration.subscription_plan.name}"

    def is_full(self):
        """Kiểm tra gói đã đầy người dùng chưa"""
        return self.buyers.count() >= self.max_users
    @staticmethod
    def find_available_group(subscription_plan_duration):
        """Tìm một gói trống dựa trên thời hạn"""
        return AccountGroup.objects.filter(
                subscription_duration=subscription_plan_duration
            ).annotate(
                buyers_count=models.Count('buyers')
            ).filter(
                buyers_count__lt=models.F('max_users')
            ).first()