# Generated by Django 3.0.8 on 2020-08-09 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20200808_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address_line1',
            field=models.CharField(blank=True, max_length=1024),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(blank=True, max_length=189),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=90),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, max_length=189),
        ),
        migrations.AlterField(
            model_name='address',
            name='zip_code',
            field=models.CharField(blank=True, max_length=18),
        ),
    ]
