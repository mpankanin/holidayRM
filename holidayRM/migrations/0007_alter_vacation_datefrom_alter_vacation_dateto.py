# Generated by Django 5.0.4 on 2024-06-03 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidayRM', '0006_vacation_is_approved_alter_vacation_datefrom_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='dateFrom',
            field=models.DateField(default=datetime.datetime(2024, 6, 3, 21, 12, 53, 175948, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='vacation',
            name='dateTo',
            field=models.DateField(default=datetime.datetime(2024, 6, 3, 21, 12, 53, 175948, tzinfo=datetime.timezone.utc)),
        ),
    ]
