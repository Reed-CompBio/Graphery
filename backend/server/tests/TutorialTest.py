from django.db import IntegrityError
from django.test import TestCase
from backend.models import *


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
    def setUp(self):
        self.tutorial = Tutorial.objects.create(url='this-is-url')

        self.default_category = Category.objects.create()
        self.tutorial.categories.add(self.default_category)
        self.new_category = Category.objects.create(category='new category')

    def test_init(self):
        self.assertEqual(self.tutorial.url, 'this-is-url')

    def test_empty_url(self):
        with self.assertRaises(IntegrityError):
            # TODO something's wrong here
            tutorial = Tutorial.objects.create()

    def test_category_linking(self):
        self.tutorial.categories.add(self.new_category)
        self.assertEqual(self.tutorial.categories.all()[0].category, self.new_category.category)

    def test_access_through_category(self):
        self.assertIn(self.tutorial, self.default_category.tutorial_set.all())


class GraphTest(TestCase):
    def test_graph_url(self):
        pass

    def test_graph_empty_url(self):
        pass

    def test_graph_priority(self):
        pass

    def test_tutorial_linking(self):
        pass

    def test_access_through_tutorial(self):
        pass

    def test_content(self):
        pass


class CodeTest(TestCase):
    def test_code_content(self):
        pass

    def test_tutorial_linking(self):
        pass

    def test_tutorial_access(self):
        pass


class ResultJsonTest(TestCase):
    def test_code_linking(self):
        pass

    def test_graph_linking(self):
        pass

    def test_unique_together(self):
        pass

    def test_code_access(self):
        pass

    def test_graph_access(self):
        pass

    def test_content(self):
        pass
