# Generated by Django 5.1.3 on 2024-12-15 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0003_coupon_times_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Hiển thị trong đơn hàng'),
        ),
        migrations.AlterField(
            model_name='coupon',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Hoạt động'),
        ),
    ]