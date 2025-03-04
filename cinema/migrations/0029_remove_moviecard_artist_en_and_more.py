# Generated by Django 5.0 on 2024-04-09 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0028_moviecard_artist_en_moviecard_artist_uk_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="moviecard",
            name="artist_en",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="artist_uk",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="director_en",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="director_uk",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="genre_en",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="genre_uk",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="melodist_en",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="melodist_uk",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="screenwriter_en",
        ),
        migrations.RemoveField(
            model_name="moviecard",
            name="screenwriter_uk",
        ),
    ]
