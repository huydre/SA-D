# Generated by Django 4.2 on 2025-02-19 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="books/"),
        ),
    ]
