# Generated by Django 4.2.3 on 2023-07-08 20:05

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course_registration", "0007_userprofile_slug"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="slug",
        ),
    ]