# Generated by Django 5.0 on 2024-01-22 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0011_newsevents_seo_block'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
