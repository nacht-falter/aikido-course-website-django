# Documentation for defining choices for CharFields:
# https://docs.djangoproject.com/en/4.2/ref/models/fields/#choices
# Assign increasing integer values to a list of variables:
# https://stackoverflow.com/a/64485228
(
    RED_BELT,
    SIXTH_KYU,
    FIFTH_KYU,
    FOURTH_KYU,
    THIRD_KYU,
    SECOND_KYU,
    FIRST_KYU,
    SHODAN,
    NIDAN,
    SANDAN,
    YONDAN,
    GODAN,
    ROKUDAN,
) = range(13)

(
    BANK,
    CASH,
) = range(2)

PAYMENT_STATUS = ((0, "Unpaid"), (1, "Paid"))

PAYMENT_METHODS = (
    (BANK, "Bank Transfer"),
    (CASH, "Cash"),
)

EXAM_GRADE_CHOICES = (
    (SIXTH_KYU, "7th Kyu ⚪️"),
    (FIFTH_KYU, "5th Kyu 🟡"),
    (FOURTH_KYU, "4th Kyu 🟠"),
    (THIRD_KYU, "3rd Kyu 🟢"),
    (SECOND_KYU, "2nd Kyu 🔵"),
    (FIRST_KYU, "1st Kyu 🟤"),
)

GRADE_CHOICES = (
    (RED_BELT, "Red Belt 🔴"),
    (SIXTH_KYU, "6th Kyu ⚪️"),
    (FIFTH_KYU, "5th Kyu 🟡"),
    (FOURTH_KYU, "4th Kyu 🟠"),
    (THIRD_KYU, "3rd Kyu 🟢"),
    (SECOND_KYU, "2nd Kyu 🔵"),
    (FIRST_KYU, "1st Kyu 🟤"),
    (SHODAN, "1st Dan ⚫️"),
    (NIDAN, "2nd  Dan ⚫️"),
    (SANDAN, "3rd Dan ⚫️"),
    (YONDAN, "4th Dan ⚫️"),
    (GODAN, "5th Dan ⚫️"),
    (ROKUDAN, "6th Dan ⚫️"),
)

DOJO_CHOICES = (
    ("AAR", "Aikido am Rhein"),
    ("AVE", "Aikido Verein Emmendingen"),
    ("AVF", "Aikido Verein Freiburg"),
    ("TVD", "Turnverein Denzlingen"),
    ("other", "Other Dojo"),
)

WEEKDAYS = (
    (0, "Monday"),
    (1, "Tuesday"),
    (2, "Wednesday"),
    (3, "Thursday"),
    (4, "Friday"),
    (5, "Saturday"),
    (6, "Sunday"),
)
