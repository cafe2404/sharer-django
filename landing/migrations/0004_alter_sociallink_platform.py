# Generated by Django 5.1.4 on 2024-12-17 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_landingpagecontent_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sociallink',
            name='platform',
            field=models.CharField(choices=[('Facebook', 'Facebook'), ('Telegram', 'Telegram'), ('Zalo', 'Zalo')], default='Facebook', max_length=20, verbose_name='Nền tảng mạng xã hội'),
        ),
    ]
