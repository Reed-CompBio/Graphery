from django.db import IntegrityError
from django.test import TestCase
from backend.models import Category, Tutorial


class CategoryTest(TestCase):
    def test_category_default(self):
        category = Category.objects.create()
        self.assertEqual(category.category, 'uncategorized')

    def test_category_naming(self):
        category = Category.objects.create(category='a category')
        self.assertEqual(category.category, 'a category')

    def test_category_unique(self):
        Category.objects.create()
        with self.assertRaises(IntegrityError):
            Category.objects.create()


class TutorialAnchorTest(TestCase):
    def test_init(self):
        tutorial = Tutorial(url='this-is-url')
        self.assertEqual(tutorial.url, 'this-is-url')

    def test_empty_url(self):
        with self.assertRaises(IntegrityError):
            tutorial = Tutorial.objects.create()

    def test_category_linking(self):
        category = Category.objects.create()
        tutorial = Tutorial.objects.create(url='a-default-url')
        tutorial.categories.add(category)
        self.assertEqual(tutorial.categories.all()[0].category, category.category)

    
