# Generated by Django 4.2.3 on 2023-07-21 17:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course_registration", "0030_category_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="slug",
        ),
    ]
