# Generated by Django 5.0 on 2024-04-03 11:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0026_backgroundbanner'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='seo_block',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cinema.seoblock'),
            preserve_default=False,
        ),
    ]
