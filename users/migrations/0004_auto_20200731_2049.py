# Generated by Django 3.0.8 on 2020-08-01 00:49

from django.db import migrations, models
import eventtools.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200731_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(blank=True, default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pickupinfo',
            name='instructions',
            field=models.CharField(blank=True, default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='schedule',
            name='repeat',
            field=eventtools.models.ChoiceTextField(blank=True, choices=[(None, 'No Repeat'), ('RRULE:FREQ=DAILY', 'Daily'), ('RRULE:FREQ=WEEKLY', 'Weekly'), ('RRULE:FREQ=MONTHLY', 'Monthly'), ('RRULE:FREQ=YEARLY', 'Yearly')], default=''),
        ),
    ]
