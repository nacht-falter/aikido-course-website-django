# Generated by Django 4.2.3 on 2023-07-12 19:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course_registration", "0015_courseregistration_exam_grade_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="courseregistration",
            name="exam_grade",
        ),
        migrations.AddField(
            model_name="courseregistration",
            name="grade",
            field=models.IntegerField(
                choices=[
                    (0, "No Grade 🔴"),
                    (1, "6th Kyu ⚪️"),
                    (2, "5th Kyu 🟡"),
                    (3, "4th Kyu 🟠"),
                    (4, "3rd Kyu 🟢"),
                    (5, "2nd Kyu 🔵"),
                    (6, "1st Kyu 🟤"),
                    (7, "1st Dan ⚫️"),
                    (8, "2nd  Dan ⚫️"),
                    (9, "3rd Dan ⚫️"),
                    (10, "4th Dan ⚫️"),
                    (11, "5th Dan ⚫️"),
                    (12, "6th Dan ⚫️"),
                ],
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="grade",
            field=models.IntegerField(
                choices=[
                    (0, "No Grade 🔴"),
                    (1, "6th Kyu ⚪️"),
                    (2, "5th Kyu 🟡"),
                    (3, "4th Kyu 🟠"),
                    (4, "3rd Kyu 🟢"),
                    (5, "2nd Kyu 🔵"),
                    (6, "1st Kyu 🟤"),
                    (7, "1st Dan ⚫️"),
                    (8, "2nd  Dan ⚫️"),
                    (9, "3rd Dan ⚫️"),
                    (10, "4th Dan ⚫️"),
                    (11, "5th Dan ⚫️"),
                    (12, "6th Dan ⚫️"),
                ],
                default=0,
            ),
        ),
    ]
