# Generated by Django 5.0.4 on 2024-06-03 21:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('holidayRM', '0007_alter_vacation_datefrom_alter_vacation_dateto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vacation',
            name='dateFrom',
        ),
        migrations.RemoveField(
            model_name='vacation',
            name='dateTo',
        ),
        migrations.AddField(
            model_name='vacation',
            name='date_from',
            field=models.DateField(default=datetime.datetime(2024, 6, 3, 21, 51, 53, 851026, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='vacation',
            name='date_to',
            field=models.DateField(default=datetime.datetime(2024, 6, 3, 21, 51, 53, 851026, tzinfo=datetime.timezone.utc)),
        ),
    ]
