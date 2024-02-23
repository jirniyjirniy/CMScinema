# Generated by Django 5.0 on 2024-01-22 14:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0013_alter_pages_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='seo_block',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cinema.seoblock'),
            preserve_default=False,
        ),
    ]
