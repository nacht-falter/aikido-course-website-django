# Generated by Django 4.2.3 on 2023-07-10 08:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course_registration", "0012_userprofile_first_name_userprofile_last_name"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="userprofile",
            name="last_name",
        ),
    ]