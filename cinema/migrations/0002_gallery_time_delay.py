# Generated by Django 5.0 on 2023-12-27 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='time_delay',
            field=models.PositiveSmallIntegerField(default=10000),
        ),
    ]
