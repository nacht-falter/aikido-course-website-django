from django.db import migrations, models

# Course types that allowed exams before has_exam was introduced
LEGACY_EXAM_COURSES = [
    "sensei_emmerson",
    "external_teacher",
    "dan_bw_teacher",
    "hombu_dojo",
]


def enable_exam_for_legacy_courses(apps, schema_editor):
    InternalCourse = apps.get_model("courses", "InternalCourse")
    InternalCourse.objects.filter(
        course_type__in=LEGACY_EXAM_COURSES,
    ).exclude(
        fee_category="dan_seminar",
    ).update(has_exam=True)


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0013_alter_accommodationoptiontranslation_unique_together_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="internalcourse",
            name="has_exam",
            field=models.BooleanField(
                default=False,
                help_text="Participants can apply for an exam when registering.",
                verbose_name="Course with Exam",
            ),
        ),
        migrations.RunPython(
            enable_exam_for_legacy_courses, migrations.RunPython.noop
        ),
    ]
