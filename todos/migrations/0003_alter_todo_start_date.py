# Generated by Django 4.0.5 on 2022-06-14 05:03

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2022, 6, 14, 5, 3, 22, 301914, tzinfo=utc)),
        ),
    ]