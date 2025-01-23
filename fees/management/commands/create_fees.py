import json
from itertools import product

from django.core.management.base import BaseCommand

from courses.models import CourseSession, InternalCourse
from danbw_website import constants
from fees.models import Fee


def load_price_matrix():
    """Load the price matrix from a JSON file. The price matrix must be a nested dictionary with the following structure:
    {
        "course_type": {
            "fee_category": {
                "fee_type": {
                    "amount": 0.0,
                    "cash_fee": 0.0,
                    "external_fee": 0.0
                }
            }
        }
    }
    """
    with open("fees/price_matrix.json", "r") as file:
        return json.load(file)


class Command(BaseCommand):
    help = "Create all fees based on the predefined price matrix"

    def handle(self, *args, **kwargs):
        fee_counter = 0
        exists_counter = 0
        skipped_counter = 0
        counters = {
            "sensei_emmerson": 0,
            "hombu_dojo": 0,
            "external_teacher": 0,
            "dan_bw_teacher": 0,
            "children": 0,
        }
        created_fees = []
        existing_fees = []
        skipped_fees = []

        price_matrix = load_price_matrix()

        self.stdout.write("Creating fees...\n\n")

        for course_type, fee_category, fee_type in product(
            constants.COURSE_TYPES,
            constants.FEE_CATEGORIES,
            Fee.FEE_TYPES,
        ):
            try:
                amount = price_matrix.get(course_type[0], {}).get(
                    fee_category[0], {}).get(fee_type[0], {}).get("amount")
                extra_fee_cash = price_matrix.get(course_type[0], {}).get(
                    fee_category[0], {}).get(fee_type[0], {}).get("cash_fee")
                extra_fee_external = price_matrix.get(course_type[0], {}).get(
                    fee_category[0], {}).get(fee_type[0], {}).get("external_fee")

                if amount is not None:
                    created = Fee.objects.get_or_create(
                        course_type=course_type[0],
                        fee_category=fee_category[0],
                        fee_type=fee_type[0],
                        amount=amount,
                        extra_fee_cash=extra_fee_cash if extra_fee_cash is not None else 0,
                        extra_fee_external=extra_fee_external if extra_fee_external is not None else 0,
                    )[1]
                    if created:
                        created_fees.append(
                            (course_type[0], fee_category[0], fee_type[0]))
                        fee_counter += 1
                        counters[course_type[0]] += 1
                    else:
                        existing_fees.append(
                            (course_type[0], fee_category[0], fee_type[0]))
                        exists_counter += 1
                else:
                    skipped_fees.append(
                        (course_type[0], fee_category[0], fee_type[0]))
                    skipped_counter += 1

            except Exception as e:
                self.stderr.write(
                    f"Error processing combination: {course_type}, {fee_category}, {fee_type}"
                )
                self.stderr.write(f"Error: {str(e)}")
                continue

        for course_type, fee_category, fee_type in created_fees:
            self.stdout.write(
                f"Created fee for {course_type}, {fee_category}, {fee_type}"
            )

        for course_type, fee_category, fee_type in existing_fees:
            self.stdout.write(
                f"Fee already existed for {course_type}, {fee_category}, {fee_type}"
            )

        for course_type, fee_category, fee_type in skipped_fees:
            self.stdout.write(
                f"Fee not found for {course_type}, {fee_category}, {fee_type}."
            )

        self.stdout.write(f"\nTotal fees created: {fee_counter}")
        for course_type, count in counters.items():
            self.stdout.write(f"Total {course_type} fees created: {count}")
        self.stdout.write(f"\nTotal fees already existed: {exists_counter}")
        self.stdout.write(f"\nTotal combinations skipped: {skipped_counter}")
