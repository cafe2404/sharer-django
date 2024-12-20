# Generated by Django 5.1.3 on 2024-12-15 02:38

import coupons.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupons', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'ordering': ['-expiration_date'], 'verbose_name': 'Mã giảm giá', 'verbose_name_plural': 'Mã giảm giá'},
        ),
        migrations.AlterField(
            model_name='coupon',
            name='code',
            field=models.CharField(default=coupons.models.generate_random_code, max_length=20, unique=True, verbose_name='Mã giảm giá'),
        ),
    ]
