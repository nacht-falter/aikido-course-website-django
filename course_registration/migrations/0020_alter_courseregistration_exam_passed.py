# Generated by Django 4.2.3 on 2023-07-12 21:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course_registration", "0019_courseregistration_exam_passed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="courseregistration",
            name="exam_passed",
            field=models.BooleanField(),
        ),
    ]