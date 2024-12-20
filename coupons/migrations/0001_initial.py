# Generated by Django 5.1.3 on 2024-12-14 15:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Mã giảm giá')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Mô tả')),
                ('discount_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Giảm giá (số tiền)')),
                ('additional_days', models.PositiveIntegerField(blank=True, null=True, verbose_name='Ngày cộng thêm')),
                ('usage_limit', models.PositiveIntegerField(default=1, verbose_name='Số lần sử dụng tối đa')),
                ('expiration_date', models.DateTimeField(verbose_name='Ngày hết hạn')),
                ('is_active', models.BooleanField(default=True, verbose_name='Còn hiệu lực')),
            ],
        ),
        migrations.CreateModel(
            name='UserCoupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('used_at', models.DateTimeField(auto_now_add=True, verbose_name='Thời gian sử dụng')),
                ('is_used', models.BooleanField(default=False, verbose_name='Đã sử dụng')),
                ('coupon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coupons.coupon', verbose_name='Mã giảm giá')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Người dùng')),
            ],
        ),
    ]
