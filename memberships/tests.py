from django.contrib.admin.sites import site
from django.test import TestCase

from .admin import toggle_passport_issued
from .models import ChildrensPassport, DanBwMembership, DanIntMembership


class MembershipAdminActionsTest(TestCase):
    def test_passport_toggle_only_on_models_with_passport_field(self):
        for model in (DanIntMembership, ChildrensPassport, DanBwMembership):
            has_field = any(
                f.name == "passport_issued" for f in model._meta.get_fields()
            )
            actions = site._registry[model].actions
            self.assertEqual(
                toggle_passport_issued in actions, has_field, model.__name__
            )
