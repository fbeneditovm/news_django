# Generated by Django 4.2.19 on 2025-02-24 11:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.functions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="NewsArticle",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("subtitle", models.CharField(max_length=500)),
                (
                    "image",
                    models.ImageField(
                        blank=True, upload_to="news_images/", validators=[utils.functions.validate_image_file]
                    ),
                ),
                ("draft_content", models.TextField()),
                ("published_content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("original_publication_at", models.DateTimeField()),
                ("last_publication_update_at", models.DateTimeField()),
                ("status", models.CharField(choices=[("DRAF", "Draft"), ("PUBD", "Published")], max_length=4)),
                (
                    "column",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("POW", "Power"),
                            ("TAX", "Taxes"),
                            ("HLTH", "Health"),
                            ("EN", "Energy"),
                            ("LAB", "Labor"),
                        ],
                        max_length=4,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
