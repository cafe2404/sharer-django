# Generated by Django 5.1.3 on 2024-12-03 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('platform_share', '0005_remove_platform_base_path_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='platform',
            name='name',
            field=models.CharField(choices=[('Semrush', 'Semrush'), ('Keywords Tool', 'Keywords Tool'), ('Canva', 'Canva'), ('FreePik', 'Freepik'), ('Minea', 'Minea'), ('Placeit', 'Place It'), ('Pipi Ads', 'Pipi Ads'), ('Heyesty', 'Hey Esty'), ('Dropship', 'Dropship'), ('Auto DS', 'Auto Ds')], default='Semrush', max_length=100),
        ),
    ]
