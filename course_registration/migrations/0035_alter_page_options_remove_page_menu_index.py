# Generated by Django 4.2.3 on 2023-08-04 08:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course_registration', '0034_alter_page_options_page_menu_index'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='page',
            options={},
        ),
        migrations.RemoveField(
            model_name='page',
            name='menu_index',
        ),
    ]
