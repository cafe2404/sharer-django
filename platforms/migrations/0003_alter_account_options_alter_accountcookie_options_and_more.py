# Generated by Django 5.1.3 on 2024-12-13 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0002_account_package'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='account',
            options={'verbose_name': 'Tài khoản', 'verbose_name_plural': 'Tài khoản'},
        ),
        migrations.AlterModelOptions(
            name='accountcookie',
            options={'verbose_name': 'Cookie', 'verbose_name_plural': 'Cookie'},
        ),
        migrations.AlterModelOptions(
            name='platform',
            options={'verbose_name': 'Nền tảng', 'verbose_name_plural': 'Nền tảng'},
        ),
    ]
