# Generated by Django 5.1.3 on 2024-12-15 03:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_order_package_order_coupons'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='transfer_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Tiền nhận được'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Tổng thanh toán'),
        ),
    ]