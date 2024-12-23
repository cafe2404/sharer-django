# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
import secrets
from subscriptions.models import PackageToken
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import timezone,now,timedelta


def generate_verification_code():
    return str(secrets.randbelow(900000) + 100000)

def generate_random_token(length=64):
    return get_random_string(length=length)

def generate_expiration_time():
    return now() + timedelta(minutes=10)

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    has_used_trial = models.BooleanField(default=False, verbose_name="Đã sử dụng gói trial")
    
    def __str__(self):
        return self.username
    def get_current_account_group(self):
        """Lấy gói đăng ký hiện tại của người dùng từ PackageToken"""
        token = PackageToken.objects.filter(user=self, is_active=True).first()
        return token.account_group if token else None
    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'
        ordering = ['is_staff']
class UserSession(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions',verbose_name='Người dùng')
    device_uuid = models.CharField(max_length=36, unique=True, null=True, blank=True,verbose_name='UUID thiết bị')
    is_active = models.BooleanField(default=False,verbose_name='Đang đăng nhập')
    last_login = models.DateTimeField(auto_now=True,verbose_name='Đăng nhập lần cuối')

    def __str__(self):
        return f"{self.user.username} - {'Active' if self.is_active else 'Inactive'}"
    class Meta:
        verbose_name = 'Phiên đăng nhập'
        verbose_name_plural = 'Phiên đăng nhập'
        ordering = ['-last_login']

class VerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6,default=generate_verification_code)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=True, blank=True,default=generate_expiration_time)
    def __str__(self):
        return f"Verification Code for {self.user.username}"
    
    def is_code_expired(self):
        """Check if the code is expired (valid for 10 minutes)."""
        expiration_time = self.created_at + timedelta(minutes=10)
        return now() > expiration_time
    
    # Tạo mã xác thực mới

    def reset_verification_code(self):
        self.code = generate_verification_code()
        self.expiration_time = generate_expiration_time()
        self.save()
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
            

    def send_verification_email(self):
        html_content = render_to_string('emails/verify_code.html', {'verification_code': self})
        email = EmailMessage(
            subject=f'Xác thực tài khoản {self.user.username}',
            body=html_content,
            from_email='contact@sharer.com',
            to=[self.user.email],  
        )
        email.content_subtype = "html" 
        email.send()
        
    @classmethod
    def create_or_reset_verification_code(cls, user):
        verification_code, created = cls.objects.get_or_create(user=user, is_verified=False)
        # Kiểm tra nếu không cần tạo mã mới và mã cũ hết hạn thì sẽ reset và gửi email
        if not created :
            # nếu mã cũ hết hạn
            if verification_code.is_code_expired() :
                print("Reset mã xác thực")
                verification_code.reset_verification_code()
                verification_code.send_verification_email()
        # nếu không có mã cũ mà phải tạo mã mới thì sẽ gửi mail mới
        else: 
            print("Tạo mã xác thực mới")
            verification_code.send_verification_email() 
        return verification_code
    
    def user_email_changed(self):
        self.is_verified = False
        self.save()
        