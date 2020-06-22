import textwrap
import unittest
from typing import Iterable

from django.db import IntegrityError
from graphene.test import Client
from graphene_django.utils import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase

from graphery.schema import schema
from backend.models import *

from parameterized import parameterized

import json


class GraphQLAPITest(GraphQLTestCase, JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphql'
    fixtures = ['test_data.json', ]

    standard_query = '''
        query getTutorialPost($url: String, $translation: String) {
            tutorial(url: $url) {
            id
            url
            isPublished
            categories
            content(translation: $translation){
              id
              title
              authors
              abstract
              contentHtml
              isPublished
            }
            code {
              id
              code
              isPublished
            }
            graphSet {
              id
              graphInfo
              cyjs
              isPublished
            }
          }
        }
    '''

    def get_response_and_content(self, variables: dict = None):
        response = self.query(self.standard_query, variables=variables)
        content = json.loads(response.content)
        return response, content

    def error_message_match(self, response, content, messages: Iterable[str]):
        self.assertResponseHasErrors(response)
        rep = zip(content['errors'], messages)
        self.assertTrue(all(error['message'] == message for (error, message) in rep))

    def test_fixture(self):
        user = User.objects.get(username='default_user')
        self.assertEqual(user.email, 'default@reed.edu')

    def test_tutorial_url_exist(self):
        variables = {
            'url': 'test-tutorial2'
        }
        response, content = self.get_response_and_content(variables)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['tutorial']['url'], 'test-tutorial2')

    def test_tutorial_url_not_exist(self):
        variables = {
            'url': 'test-tutorial-not-exist'
        }
        response, content = self.get_response_and_content(variables)
        self.error_message_match(response,
                                 content,
                                 ('Tutorial matching query does not exist.', ))

    @parameterized.expand([
        ('test-tutorial1', ('lol', 'like')),
        ('test-tutorial3', ('uncategorized', )),
        ('test-tutorial4', ())
    ])
    def test_tutorial_categories(self, url, expected_cat):
        variables = {
            'url': url
        }
        response, content = self.get_response_and_content(variables)
        categories = content['data']['tutorial']['categories']
        self.assertEqual(len(categories), len(expected_cat))
        self.assertTrue(all(cat in categories for cat in expected_cat))

    @parameterized.expand([
        ('test-default', ),
        ('test-tutorial1', ),
        ('test-tutorial3', )
    ])
    def test_tutorial_content_trans_exist(self, url):
        variables = {
            'url': url,
            'translation': 'zh-cn'
        }
        response, content = self.get_response_and_content(variables)
        self.assertResponseNoErrors(response)

    def test_tutorial_content_trans_not_exist(self):
        variables = {
            'url': 'test-tutorial4',
            'translation': 'zh-cn'
        }
        response, content = self.get_response_and_content(variables)
        self.error_message_match(response, content, ('This tutorial does not provide zh-cn translation for now. ', ))

    @parameterized.expand([
        ('test-tutorial3', 'zh-cn', ('author4', 'author5')),
        ('test-default', 'zh-cn', ('default_user', )),
        ('test-tutorial1', 'zh-cn', ()),

    ])
    def test_tutorial_content_authors(self, url, trans, expected_authors):
        variables = {
            'url': url,
            'translation': trans
        }
        response, content = self.get_response_and_content(variables)
        authors = content['data']['tutorial']['content']['authors']
        self.assertEqual(len(authors), len(expected_authors))
        self.assertTrue(all(e_author in authors for e_author in expected_authors))

    def test_code_exist(self):
        variable = {
            'url': 'test-default'
        }
        response, content = self.get_response_and_content(variable)
        code = content['data']['tutorial']['code']
        self.assertResponseNoErrors(response)
        self.assertEqual(code['id'], '27214739-a9aa-457f-9d71-d29d36bb19f6')
        self.assertEqual(code['code'], textwrap.dedent('''
            def hello():
               print('hello world :)')
            '''))


    def test_code_not_exist(self):
        pass

    def test_graph_exist(self):
        pass

    def test_graphs_not_exist(self):
        pass

    def test_graph_ranking(self):
        pass

    def test_code_exec_json_exist(self):
        pass

    def test_code_exec_json_not_exist(self):
        pass

    def test_all_tutorial_inf(self):
        pass

    def test_published_field(self):
        pass

    def test_sorting(self):
        pass

    def test_tutorial_anchor_get(self):
        client = Client(schema=schema)
        query = '''
            query getTutorialPost($url: String, $translation: String="en-us") {
                tutorial(url: $url) {   
                content(translation: $translation) {
                  authors
                  abstract
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
