from django.db import IntegrityError
from django.test import TestCase
from backend.models import *
from graphene_django.utils.testing import GraphQLTestCase
from graphery.schema import schema
from graphene.test import Client
from graphql_jwt.testcases import JSONWebTokenTestCase
import json


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


class GraphQLAPITest(GraphQLTestCase, JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['test_data.json', ]

    def test_fixture(self):
        user = User.objects.get(username='default_user')
        self.assertEqual(user.email, 'default@reed.edu')

    def test_tutorial_anchor_get(self):
        client = Client(schema=schema)
        query = '''
            query getTutorialPost($url: String, $translation: String="en-us") {
                tutorial(url: $url) {   
                content(translation: $translation) {
                  authors
                  contentMd
                  contentHtml
                }
                code {
                  id
                  code
                }
                graphSet {
                  id
                  cyjs
                  execresultjsonSet {
                    id
                  }
                }
              }
            }
        '''
        variables = {
            "url": "test-tutorial3",
            "translation": "zhcn"
        }
        response = client.execute(query, variables=variables)
        print(response)

    def test_login_and_get_user_info(self):
        response = self.client.execute('''
            mutation {
                tokenAuth(username: "default_user", password: "password") {
                    payload
                    refreshExpiresIn
                    token
                }
            }
        ''')
        print(response)
        info_response = self.client.execute('''
            query {
                userInfo {
                    id
                    email
                    role
                    isVerified
                    dateJoined
                }
            }
        ''')
        print(info_response)

    # def test_get_user_info(self):

