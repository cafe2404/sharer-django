# Generated by Django 5.1.3 on 2024-12-05 13:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_share', '0009_remove_platformaccount_user_platformaccount_users'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('accounts', models.ManyToManyField(related_name='groups', to='platform_share.platformaccount')),
                ('users', models.ManyToManyField(related_name='account_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]