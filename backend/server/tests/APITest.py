import textwrap
from typing import Iterable

from graphene_django.utils import GraphQLTestCase

from graphery.schema import schema
from backend.models import *

from parameterized import parameterized

import json


class GraphQLAPITest(GraphQLTestCase):
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
              priority
              graphInfo
              cyjs
              isPublished
            }
          }
        }
    '''

    def get_response_and_content(self, query=standard_query, variables: dict = None):
        response = self.query(query, variables=variables)
        content = json.loads(response.content)
        return response, content

    def get_user_info(self):
        return self.get_response_and_content(query='''
            query {
                userInfo {
                    id
                    username
                }
            }
        ''')

    def login_as_su(self):
        response, content = self.get_response_and_content(
            query='''
                mutation {
                    tokenAuth(username: "super_user", password: "password") {
                        payload
                        refreshExpiresIn
                        token
                    }
                }
            '''
        )
        self.assertResponseNoErrors(response)
        login_rep, login_content = self.get_user_info()
        self.assertResponseNoErrors(login_rep)
        self.assertEqual(login_content['data']['userInfo']['username'], 'super_user')

    def reset_login(self):
        from http.cookies import SimpleCookie
        self._client.cookies = SimpleCookie()

    def error_message_match(self, response, content, messages: Iterable[str]):
        self.assertResponseHasErrors(response)
        rep = zip(content['errors'], messages)
        self.assertTrue(all(error['message'] == message for (error, message) in rep))

    def test_fixture(self):
        user = User.objects.get(username='default_user')
        self.assertEqual(user.email, 'default@reed.edu')

    @parameterized.expand([
        ('test-tutorial1',),
        ('test-tutorial3',),
        ('test-tutorial4',),
        ('test-tutorial5',),
        ('test-default',),
    ])
    def test_tutorial_url_exist(self, url):
        variables = {
            'url': url
        }
        response, content = self.get_response_and_content(variables=variables)
        self.assertResponseNoErrors(response)
        self.assertEqual(content['data']['tutorial']['url'], url)

    @parameterized.expand([
        ('test-tutorial-not-exist',
         'The tutorial you requested with url=test-tutorial-not-exist, id=None does not exist.'
         ),
        ('test-tutorial2', 'The tutorial you requested with url=test-tutorial2, id=None does not exist.'),
        (None, 'In tutorial query, the url and id arguments can not both be empty.')
    ])
    def test_tutorial_url_not_exist(self, url, msg):
        variables = {
            'url': url
        }
        response, content = self.get_response_and_content(variables=variables)
        self.error_message_match(response,
                                 content,
                                 (msg, ))

    @parameterized.expand([
        ('test-tutorial1', ('like',)),
        ('test-tutorial3', ('uncategorized',)),
        ('test-tutorial4', ())
    ])
    def test_tutorial_categories_published_only(self, url, expected_cat):
        variables = {
            'url': url
        }
        response, content = self.get_response_and_content(variables=variables)
        categories = content['data']['tutorial']['categories']
        self.assertEqual(len(categories), len(expected_cat))
        self.assertTrue(all(cat in categories for cat in expected_cat))

    @parameterized.expand([
        ('test-default',),
        ('test-tutorial1',),
        ('test-tutorial3',)
    ])
    def test_tutorial_content_trans_exist(self, url):
        variables = {
            'url': url,
            'translation': 'zh-cn'
        }
        response, content = self.get_response_and_content(variables=variables)
        self.assertResponseNoErrors(response)

    def test_tutorial_content_trans_not_exist(self):
        variables = {
            'url': 'test-tutorial4',
            'translation': 'zh-cn'
        }
        response, content = self.get_response_and_content(variables=variables)
        self.error_message_match(response, content, ('This tutorial does not provide zh-cn translation for now. ',))

    @parameterized.expand([
        # removed author 5 since it does not exist
        ('test-tutorial3', 'zh-cn', ('author4', )),
        ('test-default', 'zh-cn', ('default_user',)),
        ('test-tutorial1', 'zh-cn', ()),

    ])
    def test_tutorial_content_authors(self, url, trans, expected_authors):
        variables = {
            'url': url,
            'translation': trans
        }
        response, content = self.get_response_and_content(variables=variables)
        authors = content['data']['tutorial']['content']['authors']
        self.assertEqual(len(authors), len(expected_authors))
        self.assertTrue(all(e_author in authors for e_author in expected_authors))

    def test_code_exist(self):
        variable = {
            'url': 'test-default'
        }
        response, content = self.get_response_and_content(variables=variable)
        code = content['data']['tutorial']['code']
        self.assertResponseNoErrors(response)
        self.assertEqual(code['id'], '27214739-a9aa-457f-9d71-d29d36bb19f6')
        self.assertEqual(code['code'], textwrap.dedent('''
            def hello():
               print('hello world :)')
            '''))

    def test_code_not_exist(self):
        variable = {
            'url': 'test-tutorial1'
        }
        response, content = self.get_response_and_content(variables=variable)
        code = content['data']['tutorial']['code']
        self.assertResponseNoErrors(response)
        self.assertEqual(code['id'], '00000000-0000-0000-0000-000000000000')
        self.assertEqual(code['code'], '# Empty \n')

    def test_graph_exist(self):
        variables = {
            'url': 'test-default'
        }
        response, content = self.get_response_and_content(variables=variables)
        graph_set = content['data']['tutorial']['graphSet']
        self.assertEqual(len(graph_set), 2)

    def test_graphs_not_exist(self):
        variables = {
            'url': 'test-tutorial4'
        }
        response, content = self.get_response_and_content(variables=variables)
        graph_set = content['data']['tutorial']['graphSet']
        self.assertEqual(len(graph_set), 0)

    def test_graph_ranking(self):
        variables = {
            'url': 'test-default'
        }
        response, content = self.get_response_and_content(variables=variables)
        graph_set = content['data']['tutorial']['graphSet']
        self.assertEqual(len(graph_set), 2)
        for graph in graph_set:
            self.assertIn('priority', graph)

    def test_code_exec_json_exist(self):
        pass

    def test_code_exec_json_not_exist(self):
        pass

    @parameterized.expand([
        ('en-us', '', False),
        ('zh-cn', '', True),
        ('zh-cn', 'en-us', False)
    ])
    def test_all_tutorial_inf(self, trans: str, default: str, has_error: bool):
        query = '''
            query allTutorialInfo($translation: String, $default: String){
              allTutorialInfo {
                url
                content(translation: $translation, default: $default) {
                  title
                  authors
                  abstract
                  modifiedTime
                }
              }
            }
        '''
        variables = {
            'translation': trans,
            'default': default,
        }
        response, content = self.get_response_and_content(query=query, variables=variables)
        if has_error:
            self.assertResponseHasErrors(response)
        else:
            self.assertResponseNoErrors(response)

    def test_all_graph_info(self):
        graph_query = '''
            query {
               allGraphInfo {
                id
              }
            }
        '''
        response, content = self.get_response_and_content(query=graph_query)
        self.assertResponseNoErrors(response)
        self.assertEqual(len(content['data']['allGraphInfo']), 2)

    def test_published_field(self):
        self.login_as_su()

        # published tutorial vs not published tutorial
        t2_variables = {
            'url': 'test-tutorial2'
        }
        t2_response, t2_content = self.get_response_and_content(variables=t2_variables)
        self.assertResponseNoErrors(t2_response)
        self.assertEqual(t2_content['data']['tutorial']['url'], 'test-tutorial2')

        # published tutorial not published attrs like content, authors(is_active actually),
        td_variables = {
            'url': 'test-default'
        }
        td_response, td_content = self.get_response_and_content(variables=td_variables)
        self.assertResponseNoErrors(td_response)
        self.assertEqual(len(td_content['data']['tutorial']['graphSet']), 3)

        # published graph vs not published graph
        graph_query = '''
            query {
               allGraphInfo {
                id
              }
            }
        '''
        g_response, g_content = self.get_response_and_content(query=graph_query)
        self.assertResponseNoErrors(g_response)
        self.assertEqual(len(g_content['data']['allGraphInfo']), 3)

        # published categories vs not published categories
        cat_query = '''
           query {
                allCategories {
                    category
                }
            }
        '''
        t2_response,  t2_content = self.get_response_and_content(query=cat_query)
        self.assertResponseNoErrors(t2_response)
        expected_cats = ({'category': 'like'}, {'category': 'lol'}, {'category': 'uncategorized'})
        cats: list =  t2_content['data']['allCategories']
        self.assertEqual(len(expected_cats), len(cats))
        self.assertTrue(all(expected_cat in cats for expected_cat in expected_cats))
        self.reset_login()

    def test_sorting(self):
        pass

    def test_login_and_get_user_info_reset_test(self):
        # self.client.login(user)
        username = 'default_user'
        response = self.query('''
            mutation {
                tokenAuth(username: "%s", password: "password") {
                    payload
                    refreshExpiresIn
                    token
                }
            }
        ''' % username)
        self.assertResponseNoErrors(response)
        response, content = self.get_response_and_content('''
            query {
                userInfo {
                    username
                }
            }
        ''')
        self.assertEqual(content['data']['userInfo']['username'], username)
        self.reset_login()
        response, content = self.get_response_and_content('''
            query {
                userInfo {
                    username
                }
            }
        ''')
        self.assertResponseHasErrors(response)
        self.error_message_match(response, content, ('You do not have permission to perform this action', ))
