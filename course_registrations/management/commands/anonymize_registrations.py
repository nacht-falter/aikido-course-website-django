from collections import Counter

from django.core.management.base import BaseCommand
from django.db import transaction

from course_registrations.models import CourseRegistration


class Command(BaseCommand):
    help = (
        "Anonymizes registrations of guests and deactivated accounts for courses "
        "that ended two or more calendar years ago. Run regularly from cron."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Only show what would be anonymized.",
        )

    def handle(self, *args, **options):
        registrations = CourseRegistration.due_for_anonymization().select_related(
            "course", "user"
        )
        by_year = Counter(r.course.end_date.year for r in registrations)

        if not by_year:
            self.stdout.write("Nothing to anonymize.")
            return

        for year, count in sorted(by_year.items()):
            self.stdout.write(f"{year}: {count} registrations")

        if options["dry_run"]:
            self.stdout.write("Dry run, nothing changed.")
            return

        with transaction.atomic():
            for registration in registrations:
                registration.anonymize()
        self.stdout.write(
            self.style.SUCCESS(f"Anonymized {sum(by_year.values())} registrations.")
        )
