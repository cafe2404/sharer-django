# Generated by Django 5.1.4 on 2024-12-22 10:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('platforms', '0019_platform_featrures'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platform',
            name='featrures',
        ),
    ]