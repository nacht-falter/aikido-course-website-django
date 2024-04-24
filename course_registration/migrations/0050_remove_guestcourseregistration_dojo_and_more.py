# Generated by Django 4.2.3 on 2024-04-19 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_registration', '0049_guestcourseregistration_dojo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='guestcourseregistration',
            name='dojo',
        ),
        migrations.AddField(
            model_name='guestcourseregistration',
            name='grade',
            field=models.IntegerField(choices=[(0, 'Red Belt 🔴'), (1, '6th Kyu ⚪️'), (2, '5th Kyu 🟡'), (3, '4th Kyu 🟠'), (4, '3rd Kyu 🟢'), (5, '2nd Kyu 🔵'), (6, '1st Kyu 🟤'), (7, '1st Dan ⚫️'), (8, '2nd  Dan ⚫️'), (9, '3rd Dan ⚫️'), (10, '4th Dan ⚫️'), (11, '5th Dan ⚫️'), (12, '6th Dan ⚫️')], default=0),
        ),
    ]