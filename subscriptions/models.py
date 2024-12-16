from django.db import models
from django.utils.crypto import get_random_string
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

def generate_random_token(length=64):
    return get_random_string(length=length)
# Kế hoạch đăng ký (SubscriptionPlan)
class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    platforms = models.ManyToManyField('platforms.Platform', related_name='package_templates')  # Các nền tảng hỗ trợ
    level = models.PositiveIntegerField(default=1)  # Cấp độ
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['level']
        verbose_name = "Kế hoạch"
        verbose_name_plural = "Kế hoạch"
class SubscriptionPlanDuration(models.Model):
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        related_name='durations',
        on_delete=models.CASCADE,
        verbose_name="Kế hoạch"
    )
    duration = models.PositiveIntegerField(verbose_name='Thời gian gói')  # Thời gian đăng ký (tháng)
    price = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Giá hiện tại')  # Giá hiện tại
    pre_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,verbose_name='Giá gốc')  # Giá gốc
    def price_per_month(self):
        """Tính giá mỗi tháng dựa trên tổng giá và thời gian đăng ký."""
        return round(self.price / self.duration) if self.duration > 0 else 0
    def __str__(self):
        return f"{self.subscription_plan.name} - {self.duration} tháng - {self.price} VND"
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
# Gói đăng ký bán cho người dùng (Package)
class Package(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    subscription_plan = models.ForeignKey(
        SubscriptionPlan, on_delete=models.CASCADE, related_name='packages'
    )
    max_users = models.PositiveIntegerField(default=10)  # Giới hạn số người dùng
    buyers = models.ManyToManyField('custom_user.CustomUser', related_name='bought_packages',null=True,blank=True)  # Danh sách người dùng đã mua gói
    class Meta:
        verbose_name = "Nhóm tài khoản"
        verbose_name_plural = "Nhóm tài khoản"
        ordering = ['-id']
    def __str__(self):
        return f"{self.name}-{self.subscription_plan.name}"

    def is_full(self):
        """Kiểm tra gói đã đầy người dùng chưa"""
        return self.buyers.count() >= self.max_users
    @staticmethod
    def find_available_package(subscription_plan_duration):
        """Tìm một gói trống dựa trên thời hạn"""
        return Package.objects.filter(
                subscription_plan=subscription_plan_duration.subscription_plan
            ).annotate(
                buyers_count=models.Count('buyers')
            ).filter(
                buyers_count__lt=models.F('max_users')
            ).first()
class PackageToken(models.Model):
    package = models.ForeignKey(
        Package, 
        on_delete=models.CASCADE,
        verbose_name='Nhóm tài khoản'
    )
    token = models.CharField(
        max_length=64,
        unique=True,
        default=generate_random_token,
        verbose_name='Mã truy cập'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    expires_at = models.DateTimeField(verbose_name='Ngày hết hạn')
    user = models.ForeignKey(
        'custom_user.CustomUser',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Người dùng'
    )
    is_active = models.BooleanField(default=False, verbose_name='Kích hoạt')

    class Meta:
        verbose_name = "Mã đăng ký"
        verbose_name_plural = "Mã đăng ký"
        unique_together = ('package', 'user')

    @classmethod
    def create_from_order(cls, order):
        """
        Tạo token từ Order.
        """
        if not order.subscription_plan or not order.subscription_duration:
            raise ValueError("Order must have a subscription plan and duration associated.")

        # Tìm gói trống phù hợp với kế hoạch đăng ký
        new_package = Package.find_available_package(order.subscription_duration)
        if not new_package:
            raise ValueError("No available package for the selected subscription plan.")

        # Tính ngày hết hạn dựa trên thời hạn gói
        expires_at = now() + relativedelta(months=order.subscription_duration.duration)

        # Tạo token mới
        return cls.objects.create(
            package=new_package,
            user=order.user,
            is_active=True,
            expires_at=expires_at
        )

    def save(self, *args, **kwargs):
        # Kiểm tra nếu có gói cũ và xóa người dùng khỏi gói cũ
        if self.user:
            previous_package_token = PackageToken.objects.filter(user=self.user, is_active=True).first()
            if previous_package_token and previous_package_token.package != self.package:
                previous_package_token.package.buyers.remove(self.user)
        # Gọi hàm lưu gốc
        super().save(*args, **kwargs)

        # Tự động thêm user vào danh sách buyers của package mới
        if self.user and self.user not in self.package.buyers.all():
            self.package.buyers.add(self.user)
            self.package.save()

    def __str__(self):
        return f"Token - {self.package.subscription_plan.name} - {self.user.username}"