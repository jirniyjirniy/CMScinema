# Generated by Django 5.0 on 2024-01-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0018_pages_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='can_delete',
            field=models.BooleanField(default=True),
        ),
    ]