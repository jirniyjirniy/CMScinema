# Generated by Django 5.0 on 2023-12-18 16:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('second_name', models.CharField(max_length=150)),
                ('nickname', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('language', models.CharField(choices=[('EN', 'English'), ('UA', 'Ukraine')], default='UA', max_length=10)),
                ('gender', models.CharField(choices=[('MALE', 'Male'), ('FEMALE', 'Female')], default='MALE', max_length=6)),
                ('card', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=30)),
                ('birth_date', models.DateField()),
                ('city', models.CharField(max_length=100)),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
