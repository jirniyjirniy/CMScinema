# Generated by Django 5.0 on 2024-01-10 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='banner',
            name='rotation_speed',
        ),
        migrations.RemoveField(
            model_name='banner',
            name='status',
        ),
        migrations.CreateModel(
            name='BannerSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rotation_speed', models.PositiveSmallIntegerField()),
                ('status', models.BooleanField(default=True)),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cinema.banner')),
            ],
        ),
    ]
