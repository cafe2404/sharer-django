# Generated by Django 5.1.3 on 2024-12-05 13:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_share', '0010_accountgroup'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='platformaccount',
            name='cookie',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='platformaccount',
            name='password',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='platformaccount',
            name='username',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='platformaccount',
            name='users',
            field=models.ManyToManyField(blank=True, related_name='platform_accounts', to=settings.AUTH_USER_MODEL, verbose_name='Người dùng'),
        ),
    ]
