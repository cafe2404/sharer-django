# Generated by Django 5.1.3 on 2024-11-20 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_share', '0002_platform_blacklist_path_platform_css_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='platform',
            name='base_path',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]