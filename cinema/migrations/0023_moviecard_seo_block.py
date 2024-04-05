# Generated by Django 5.0 on 2024-03-26 13:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0022_contacts_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='moviecard',
            name='seo_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cinema.seoblock'),
        ),
    ]
