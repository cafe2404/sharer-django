# Generated by Django 5.1.3 on 2024-12-13 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0002_delete_admininfomation'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpagecontent',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Kích hoạt'),
        ),
    ]
