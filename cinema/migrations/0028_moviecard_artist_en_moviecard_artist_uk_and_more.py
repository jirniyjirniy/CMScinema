# Generated by Django 5.0 on 2024-04-09 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cinema", "0027_contacts_seo_block"),
    ]

    operations = [
        migrations.AddField(
            model_name="moviecard",
            name="artist_en",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="artist_uk",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="desc_en",
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="desc_uk",
            field=models.TextField(max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="director_en",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="director_uk",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="genre_en",
            field=models.ManyToManyField(blank=True, null=True, to="cinema.genre"),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="genre_uk",
            field=models.ManyToManyField(blank=True, null=True, to="cinema.genre"),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="melodist_en",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="melodist_uk",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="screenwriter_en",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="screenwriter_uk",
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="title_en",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AddField(
            model_name="moviecard",
            name="title_uk",
            field=models.CharField(max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name="backgroundbanner",
            name="type",
            field=models.CharField(
                choices=[("PHOTO", "Фото на фон"), ("JUST", "Просто фон")],
                default="PHOTO",
                max_length=5,
            ),
        ),
    ]