from django.db import models

# Create your models here.
class Issue(models.Model):
    content = models.TextField(verbose_name="Nội dung")
    image = models.ImageField(upload_to='issue/', height_field=None, width_field=None, max_length=None, null=True, blank=True,verbose_name="Ảnh")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Ngày tạo")
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Vấn đề"
        verbose_name_plural = "Vấn đề"
    def __str__(self):
        return self.content