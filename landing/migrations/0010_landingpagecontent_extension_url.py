# Generated by Django 5.1.4 on 2024-12-22 23:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0009_alter_footercolumn_options_alter_footerlink_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='landingpagecontent',
            name='extension_url',
            field=models.URLField(blank=True, null=True, verbose_name='Đường dẫn tải xuống extension'),
        ),
    ]