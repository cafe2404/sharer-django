from django.db import models
from django.utils.timezone import now
from custom_user.models import CustomUser as User
from django.utils.crypto import get_random_string


def generate_random_code(length=12):
    return get_random_string(length=length)


class Coupon(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tên mã giảm giá")
    code = models.CharField(max_length=20, unique=True, default=generate_random_code, verbose_name="Mã giảm giá")
    description = models.TextField(blank=True, null=True, verbose_name="Mô tả")
    discount_amount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Giảm giá (số tiền)"
    )
    additional_days = models.PositiveIntegerField(
        blank=True, null=True, verbose_name="Ngày cộng thêm"
    )
    usage_limit = models.PositiveIntegerField(default=1, verbose_name="Số lần sử dụng tối đa")
    times_used = models.PositiveIntegerField(default=0, verbose_name="Số lần sử dụng")
    expiration_date = models.DateTimeField(verbose_name="Ngày hết hạn")
    is_active = models.BooleanField(default=True, verbose_name="Hoạt động")
    is_public = models.BooleanField(default=False, verbose_name="Hiển thị trong đơn hàng")
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True, verbose_name="Ngày cập nhật")
    class Meta:
        verbose_name = "Mã giảm giá"
        verbose_name_plural = "Mã giảm giá"
        ordering = ['-expiration_date']
    def is_valid(self):
        """Kiểm tra nếu coupon còn hiệu lực và chưa vượt qua số lần sử dụng"""
        return self.is_active and now() < self.expiration_date
    @classmethod
    def get_valid_coupon(cls, coupon_code):
        """Truy vấn mã giảm giá hợp lệ"""
        try:
            coupon = cls.objects.get(code=coupon_code.strip(), is_active=True)
            if coupon.is_valid():
                return coupon
            return None
        except cls.DoesNotExist:
            return None
    @classmethod
    def get_latest_valid_public_coupon(cls):
        """Lấy mã giảm giá public còn hiệu lực mới nhất"""
        try:
            return cls.objects.filter(
                is_public=True,
                is_active=True,
                expiration_date__gt=now()
            ).order_by('-created_at').first()
        except cls.DoesNotExist:
            return None
    def __str__(self):
        return f"{self.code} - {'Active' if self.is_active else 'Expired'}"

class UserCoupon(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Người dùng")
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, verbose_name="Mã giảm giá")
    used_at = models.DateTimeField(auto_now_add=True, verbose_name="Thời gian sử dụng")
    is_used = models.BooleanField(default=False, verbose_name="Đã sử dụng")

    def __str__(self):
        return f"{self.user.username} - {self.coupon.code} - {'Used' if self.is_used else 'Unused'}"
