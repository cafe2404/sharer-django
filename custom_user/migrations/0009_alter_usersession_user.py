# Generated by Django 5.1.4 on 2024-12-24 09:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0008_customuser_has_used_trial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersession',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='sessions', to=settings.AUTH_USER_MODEL, verbose_name='Người dùng'),
        ),
    ]