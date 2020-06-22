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

    def test_on_delete(self):
        pass


class TutorialAnchorTest(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.tutorial = Tutorial.objects.create(url='this-is-url')

        self.default_category = Category.objects.create()
        self.tutorial.categories.add(self.default_category)
        self.new_category = Category.objects.create(category='new category')

    def test_init(self):
        self.assertEqual(self.tutorial.url, 'this-is-url')

    def test_create_tutorial_with_url_not_unique(self):
        with self.assertRaises(IntegrityError):
            duplicated_tutorial = Tutorial(url='test-default')
            duplicated_tutorial.save()

    def test_create_tutorial_with_url_unique(self):
        new_tutorial = Tutorial(url='test-new')
        new_tutorial.save()

        self.assertIn(new_tutorial, Tutorial.objects.all())

    def test_create_tutorial_without_url(self):
        with self.assertRaises(IntegrityError):
            # TODO hmmmm
            error_tutorial = Tutorial(url=None)
            error_tutorial.save()

    def test_category_linking(self):
        self.tutorial.categories.add(self.new_category)
        self.assertEqual(self.tutorial.categories.all()[0].category, self.new_category.category)

    def test_access_through_category(self):
        self.assertIn(self.tutorial, self.default_category.tutorial_set.all())

    def test_tutorial_content_trans_exist(self):
        tutorial_with_trans = Tutorial.objects.get(url='test-tutorial3')
        self.assertIsNotNone(tutorial_with_trans.get_translation('zh-cn'))

    def test_tutorial_content_trans_not_exist(self):
        tutorial_without_trans = Tutorial.objects.get(url='test-tutorial2')
        self.assertIsNone(tutorial_without_trans.get_translation('zh-cn'))

    def test_code_exist(self):
        tutorial_with_code = Tutorial.objects.get(url='test-default')
        self.assertIsNotNone(getattr(tutorial_with_code, 'code', None))

    def test_code_not_exist(self):
        tutorial_without_code = Tutorial.objects.get(url='test-tutorial1')
        with self.assertRaises(Code.DoesNotExist):
            code = tutorial_without_code.code

    def test_on_delete(self):
        pass


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

    def test_on_delete(self):
        pass


class CodeTest(TestCase):
    def test_code_content(self):
        pass

    def test_tutorial_linking(self):
        pass

    def test_tutorial_access(self):
        pass

    def test_on_delete(self):
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

    def test_on_delete(self):
        pass
