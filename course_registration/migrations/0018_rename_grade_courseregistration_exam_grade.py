# Generated by Django 4.2.3 on 2023-07-12 20:36

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("course_registration", "0017_alter_courseregistration_grade_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="courseregistration",
            old_name="grade",
            new_name="exam_grade",
        ),
    ]
