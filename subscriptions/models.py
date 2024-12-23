from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta
from platforms.models import AccountGroup

def generate_random_token(length=64):
    return get_random_string(length=length)
# Kế hoạch đăng ký (SubscriptionPlan)
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255,verbose_name="Tên gói")
    description = models.CharField(max_length=500,blank=True, null=True,verbose_name="Mô tả gói")
    featrures = models.TextField(verbose_name='Tính năng',default='',blank=True)
    
    platforms = models.ManyToManyField('platforms.Platform', related_name='package_templates',verbose_name='Các nền tảng trong gói')  # Các nền tảng hỗ trợ
    level = models.PositiveIntegerField(default=0,verbose_name='Thứ tự',null=True,blank=True) 
    recommended = models.BooleanField(default=False,verbose_name='Đề xuất gói')
    is_trial = models.BooleanField(default=False,verbose_name='Gói dùng thử')
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['level']
        verbose_name = "Kế hoạch"
        verbose_name_plural = "Kế hoạch"

class SubscriptionDurationFilter(models.Model):
    name = models.CharField(max_length=255, verbose_name='Tên bộ lọc')
    duration = models.PositiveIntegerField(verbose_name='Bộ lọc thời hạn (ngày)')
    is_hot = models.BooleanField(default=False, verbose_name='Nổi bật') 
    subscription_durations = models.ManyToManyField(
        'SubscriptionPlanDuration',
        related_name='groups',
        blank=True,
        verbose_name="Thời hạn gói"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')

    def __str__(self):
        return f"{self.duration} ngày"
    class Meta:
        ordering = ['duration']
        verbose_name = "Bộ lọc thòi hạn gói"
        verbose_name_plural = "Bộ lọc thòi hạn gói"
        
class SubscriptionPlanDuration(models.Model):
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        related_name='durations',
        on_delete=models.CASCADE,
        verbose_name="Kế hoạch"
    )
    duration = models.PositiveIntegerField(verbose_name='Thời gian gói (ngày)')  # Thời gian đăng ký (tháng)
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Giá hiện tại')  # Giá hiện tại
    pre_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,verbose_name='Giá gốc')  # Giá gốc
    def price_per_month(self):
        """Tính giá mỗi tháng dựa trên tổng giá và thời gian đăng ký."""
        return round(self.price / (self.duration*30)) if self.duration > 0 else 0
    def __str__(self):
        return f"{self.subscription_plan.name} - {self.duration} ngày - {self.price} ₫"
    @property
    def discount_percentage(self):
        if self.pre_price and self.price:
            discount = ((self.pre_price - self.price) / self.pre_price) * 100
            return f"{int(discount)}%"
        return 0
    class Meta:
        ordering = ['duration']
        verbose_name = "Thời hạn gói"
        verbose_name_plural = "Thời hạn gói"
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Tự động thêm gói này vào nhóm phù hợp
        group, created = SubscriptionDurationFilter.objects.get_or_create(duration=self.duration)
        group.subscription_durations.add(self)

class PackageToken(models.Model):
    token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_random_token,
        verbose_name='Mã truy cập'
    )
    user = models.ForeignKey(
        'custom_user.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Người dùng'
    )
    account_group = models.ForeignKey(
        'platforms.AccountGroup', 
        on_delete=models.CASCADE,
        verbose_name='Nhóm tài khoản'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    expires_at = models.DateTimeField(verbose_name='Ngày hết hạn',null=True, blank=True)
    is_active = models.BooleanField(default=False, verbose_name='Kích hoạt')
    class Meta:
        verbose_name = "Mã đăng ký"
        verbose_name_plural = "Mã đăng ký"

    @classmethod
    def create_from_order(cls, order):
        """
        Tạo token từ Order.
        """
        if not order.subscription_plan or not order.subscription_duration:
            raise ValueError("Order must have a subscription plan and duration associated.")
        # Tìm gói trống phù hợp với kế hoạch đăng ký
        new_account_group = AccountGroup.find_available_group(order.subscription_duration)
        if not new_account_group:
            raise ValueError("No available package for the selected subscription plan.")
        # Tính ngày hết hạn dựa trên thời hạn gói
        expires_at = now() + relativedelta(days=order.subscription_duration.duration)
        # Tạo token mới
        return cls.objects.create(
            account_group=new_account_group,
            user=order.user,
            is_active=True,
            expires_at=expires_at
        )

    def save(self, *args, **kwargs):
        # Kiểm tra nếu có gói cũ và xóa người dùng khỏi gói cũ
        if self.user:
            previous_package_token = PackageToken.objects.filter(user=self.user, is_active=True).first()
            if previous_package_token and previous_package_token.account_group != self.account_group:
                previous_package_token.account_group.buyers.remove(self.user)
                previous_package_token.is_active = False  # Vô hiệu hóa token cũ
                previous_package_token.save()

        super().save(*args, **kwargs)

        # Tự động thêm user vào danh sách buyers của account_group mới
        if self.user and self.user not in self.account_group.buyers.all():
            self.account_group.buyers.add(self.user)
            self.account_group.save()
    def __str__(self):
        return f"Token - {self.account_group.subscription_duration} - {self.user.username}"