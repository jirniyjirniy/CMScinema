# Generated by Django 5.0 on 2024-01-29 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0021_mainpage_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
