# Generated by Django 5.1.4 on 2024-12-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0010_landingpagecontent_extension_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpagecontent',
            name='subscription_description',
            field=models.TextField(default='Tại Sharer, chúng tôi tập trung vào các thị trường nơi công nghệ, đổi mới và vốn có thể mở ra giá trị dài hạn và thúc đẩy tăng trưởng kinh tế.', verbose_name='Mô tả đăng ký'),
        ),
        migrations.AddField(
            model_name='landingpagecontent',
            name='subscription_title',
            field=models.CharField(default='Được thiết kế cho các nhóm cũng như cá nhân', max_length=500, verbose_name='Tiêu đề đăng ký'),
        ),
    ]
