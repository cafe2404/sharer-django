# Generated by Django 5.1.3 on 2024-12-08 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0005_packagetoken_is_active_alter_packagetoken_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='level',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='packagetoken',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Kích hoạt'),
        ),
    ]
