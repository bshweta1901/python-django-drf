# Generated by Django 4.1.7 on 2023-03-27 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_variants_image_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="variants",
            name="image_id",
        ),
        migrations.RemoveField(
            model_name="variants",
            name="title",
        ),
    ]
