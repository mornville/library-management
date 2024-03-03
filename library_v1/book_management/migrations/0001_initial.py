# Generated by Django 5.0.2 on 2024-03-03 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Books",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("book_id", models.IntegerField()),
                ("book_name", models.CharField(max_length=1000)),
                ("no_of_copies", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Members",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("mem_id", models.IntegerField()),
                ("member_name", models.CharField(max_length=100)),
                (
                    "books_taken",
                    models.ManyToManyField(
                        related_name="member_books", to="book_management.books"
                    ),
                ),
            ],
        ),
    ]