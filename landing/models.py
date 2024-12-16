from django.db import models

# Create your models here.
class SocialLink(models.Model):
    platform = models.CharField(max_length=20, verbose_name="Nền tảng mạng xã hội")
    url = models.URLField(verbose_name="Đường dẫn")
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name="Icon")
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
    # Contact Information
    social_links = models.ManyToManyField(SocialLink, blank=True, verbose_name="Liên kết mạng xã hội")
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_active = models.BooleanField(default=True, verbose_name="Kích hoạt")
    class Meta:
        verbose_name = "Nội dung Landing Page"
        verbose_name_plural = "Nội dung Landing Page"
    def __str__(self):
        return self.header_title
