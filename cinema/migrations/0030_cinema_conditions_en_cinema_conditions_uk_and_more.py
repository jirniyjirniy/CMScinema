# Generated by Django 5.0 on 2024-04-09 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0029_remove_moviecard_artist_en_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="cinema",
            name="conditions_en",
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="cinema",
            name="conditions_uk",
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="cinema",
            name="desc_en",
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="cinema",
            name="desc_uk",
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="cinema",
            name="title_en",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="cinema",
            name="title_uk",
            field=models.CharField(max_length=150, null=True),
        ),
    ]
