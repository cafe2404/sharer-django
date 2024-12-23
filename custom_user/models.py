# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string
import secrets
from subscriptions.models import PackageToken
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string




def generate_verification_code():
    return str(secrets.randbelow(900000) + 100000)

def generate_random_token(length=64):
    return get_random_string(length=length)

def generate_expiration_time():
    return timezone.now() + timezone.timedelta(minutes=10)

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    def __str__(self):
        return self.username
    def get_current_account_group(self):
        """Lấy gói đăng ký hiện tại của người dùng từ PackageToken"""
        token = PackageToken.objects.filter(user=self, is_active=True).first()
        return token.account_group if token else None

class VerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6,default=generate_verification_code)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField(null=True, blank=True,default=generate_expiration_time)
    def __str__(self):
        return f"Verification Code for {self.user.username}"
    
    def is_code_expired(self):
        return timezone.now() > self.expiration_time 
    
    # Tạo mã xác thực mới
    def create_verification_code(self):
        new_code = generate_verification_code()
        while VerificationCode.objects.filter(user=self.user, code=new_code).exists(): 
            new_code = generate_verification_code()
        
        self.expiration_time = generate_expiration_time()
        self.save()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.pk or not self.is_verified:
            self.send_verification_email()

    def send_verification_email(self):
        html_content = render_to_string('emails/verify_code.html', {'verification_code': self})
        email = EmailMessage(
            subject='Xác thực tài khoản sharer',
            body=html_content,
            from_email='test@example.com',
            to=[self.user.email],  
        )
        email.content_subtype = "html" 
        email.send()