from django.db import models

# Create your models here.
class SocialLink(models.Model):
    class SocialChoice(models.TextChoices):
        facebook = "Facebook"
        telegram = "Telegram"
        zalo     = "Zalo"
    platform = models.CharField(max_length=20, verbose_name="Nền tảng mạng xã hội",choices=SocialChoice.choices, default=SocialChoice.facebook)
    url = models.URLField(verbose_name="Đường dẫn")
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    class Meta:
        verbose_name = "Liên kết mạng xã hội"
        verbose_name_plural = "Liên kết mạng xã hội"

    def __str__(self):
        return f"{self.platform} - {self.url}"

class LandingPageContent(models.Model):
    # Header Section
    header_cover_image = models.ImageField(upload_to='landing/covers/', blank=True, null=True, verbose_name="Ảnh bìa header")
    header_title = models.CharField(max_length=200, verbose_name="Tiêu đề header")
    header_description = models.TextField(verbose_name="Mô tả header")
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    document_url = models.URLField(blank=True, null=True, verbose_name="Đường dẫn tài liệu sử dụng")
    extension_url = models.URLField(blank=True, null=True, verbose_name="Đường dẫn tải xuống extension")
    
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    class Meta:
        verbose_name = "Nội dung Landing Page"
        verbose_name_plural = "Nội dung Landing Page"
    def __str__(self):
        return self.header_title

class Header(models.Model):
    header_cover_image = models.ImageField(upload_to='landing/covers/', blank=True, null=True, verbose_name="Ảnh bìa header")
    header_title = models.CharField(max_length=200, verbose_name="Tiêu đề header")
    header_description = models.TextField(verbose_name="Mô tả header")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    
    class Meta:
        verbose_name = "Tiêu đề"
        verbose_name_plural = "Tiêu đề"


class FooterLink(models.Model):
    title  = models.CharField(max_length=200, verbose_name="Tiêu đề")
    url  = models.CharField(max_length=200, verbose_name="Đường dẫn")
    class Meta:
        verbose_name = "Đường dẫn chân trang"
        verbose_name_plural = "Đường dẫn chân trang"
    def __str__(self):
        return self.title
class FooterColumn(models.Model):
    title  = models.CharField(max_length=200, verbose_name="Tiêu đề")
    links  = models.ManyToManyField(FooterLink, verbose_name="Danh sách url")
    class Meta:
        verbose_name = "Cột chân trang"
        verbose_name_plural = "Cột chân trang"
    def __str__(self):
        return self.title