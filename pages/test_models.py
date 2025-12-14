from django.test import TestCase

from .models import Category, Page


class TestCategoryModel(TestCase):
    """Tests for the Category model"""

    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
        )

    def test_category_str_method_returns_title(self):
        print("\ntest_category_str_method_returns_title")
        category = Category.objects.get(translations__title="Test Category")
        self.assertEqual(str(category), "Test Category")


class TestPageModel(TestCase):
    """Tests for the Page model"""

    def setUp(self):
        self.category = Category.objects.create(
            title="Test Category",
        )
        self.page = Page.objects.create(
            title="Test Page",
            slug="test-page",
            category=self.category,
            status=0,
        )

    def test_page_str_method_returns_title(self):
        print("\ntest_page_str_method_returns_title")
        page = Page.objects.get(translations__title="Test Page")
        self.assertEqual(str(page), "Test Page")
