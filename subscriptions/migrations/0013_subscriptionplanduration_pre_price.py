# Generated by Django 5.1.3 on 2024-12-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0012_alter_packagetoken_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplanduration',
            name='pre_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]