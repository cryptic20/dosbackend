# Generated by Django 3.0.8 on 2020-08-09 02:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20200808_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='type',
            field=models.CharField(choices=[('INDIVIDUAL', 'INDIVIDUAL'), ('BULK', 'BULK'), ('COMMERCIAL', 'COMMERCIAL'), ('INDUSTRIAL', 'INDUSTRIAL')], default='Individual', max_length=100),
        ),
    ]
