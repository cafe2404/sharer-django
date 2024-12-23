from django.db import models
from django.utils.crypto import get_random_string
from coupons.models import Coupon
from decimal import Decimal

def generate_payment_code(length=12):
    return get_random_string(length=length)
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xử lý'),
        ('paid', 'Đã thanh toán'),
        ('failed', 'Thất bại'),
        ('expired', 'Hết hạn'),
    ]

    user = models.ForeignKey('custom_user.CustomUser', on_delete=models.CASCADE, verbose_name="Khách hàng")
    subscription_plan = models.ForeignKey(
        'subscriptions.SubscriptionPlan', on_delete=models.CASCADE, verbose_name="Kế hoạch"
    )

    order_id = models.CharField(
        max_length=64, unique=True, default=generate_payment_code, verbose_name="Mã đơn hàng"
    )
    coupons = models.ManyToManyField(Coupon, blank=True, related_name='orders', verbose_name="Mã giảm giá")
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True, verbose_name="Giá trị đơn hàng")
    transfer_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True,null=True, verbose_name="Tiền nhận được")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái"
    )
    subscription_duration = models.ForeignKey(
        'subscriptions.SubscriptionPlanDuration', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Gói đăng ký"
    )
    is_used = models.BooleanField(default=False,verbose_name='Đã sử dụng')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Ngày cập nhật")

    def __str__(self):
        return f"Order {self.order_id} - {self.subscription_plan.name} - {self.user.username}"
    class Meta:
        verbose_name = "Đơn hàng"
        verbose_name_plural = "Đơn hàng"
        
        
    def calculate_amount(self):
        """
        Hàm tính toán giá trị đơn hàng dựa trên SubscriptionPlanDuration và các mã giảm giá.
        Ưu tiên giảm giá theo tiền, nếu không có thì giảm theo phần trăm.
        """
        if not self.subscription_duration:
            return Decimal(0)  # Không có kế hoạch, giá trị mặc định là 0

        # Giá gốc từ SubscriptionPlanDuration
        base_amount = Decimal(self.subscription_duration.price)  # Đảm bảo giá trị là Decimal

        if not self.pk or not self.coupons.exists():
            return base_amount  # Không có mã giảm giá, trả giá gốc

        total_discount_amount = Decimal(0)  # Tổng số tiền giảm
        total_discount_percent = Decimal(0)  # Tổng phần trăm giảm

        # Duyệt qua từng coupon để tính tổng giảm giá theo số tiền và phần trăm
        for coupon in self.coupons.all():
            if coupon.discount_amount:
                total_discount_amount += coupon.discount_amount or Decimal(0)  # Cộng số tiền giảm
            elif coupon.discount_percent:
                total_discount_percent += coupon.discount_percent or Decimal(0)  # Cộng phần trăm giảm

        # Áp dụng giảm giá theo phần trăm trước
        if total_discount_percent > 0:
            discount_from_percentage = base_amount * (total_discount_percent / Decimal(100))
            base_amount -= discount_from_percentage

        # Áp dụng giảm giá theo số tiền
        if total_discount_amount > 0:
            base_amount -= total_discount_amount

        # Đảm bảo giá trị không âm
        return max(base_amount, Decimal(0))
        
    def save(self, *args, **kwargs):
        """
        Ghi đè phương thức save để tự động tính toán giá trị đơn hàng.
        """
        # Lưu lần đầu nếu đối tượng chưa có ID
        if not self.pk:
            super().save(*args, **kwargs)

        # Sau khi đã có ID, tính toán giá trị đơn hàng
        self.amount = self.calculate_amount()

        # Lưu lại lần nữa với giá trị đã cập nhật
        super().save(*args, **kwargs)
    
class PaymentSetting(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'Chuyển khoản ngân hàng'),
        # ('e_wallet', 'Ví điện tử'),
        # ('cash', 'Tiền mặt'),
    ]
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name="Phương thức thanh toán"
    )
    account_number = models.CharField(
        max_length=50,
        verbose_name="Số tài khoản"
    )
    bank_code = models.CharField(
        max_length=100,
        verbose_name="Mã ngân hàng"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Ngày tạo"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Ngày cập nhật"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Kích hoạt"
    )
    def get_payment_method(self):
        return dict(self.PAYMENT_METHOD_CHOICES).get(self.payment_method)

    def __str__(self):
        return f"{self.get_payment_method()} - {self.account_number}"

    class Meta:
        verbose_name = "Cài đặt thanh toán"
        verbose_name_plural = "Cài đặt thanh toán"
