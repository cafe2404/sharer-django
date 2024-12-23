# Generated by Django 5.1.4 on 2024-12-20 23:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0012_remove_account_thời_gian_hết_hạn_admin__and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='login_choice',
            field=models.CharField(blank=True, choices=[('cookie', 'Cookie'), ('rankerfox', 'Rankerfox'), ('adspower', 'Ads Power')], default='cookie', max_length=255, null=True, verbose_name='Phương thức đăng nhập'),
        ),
        migrations.AlterField(
            model_name='account',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Hoạt động'),
        ),
        migrations.AlterField(
            model_name='account',
            name='rented_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rented_accounts', to=settings.AUTH_USER_MODEL, verbose_name='Người mua'),
        ),
    ]
