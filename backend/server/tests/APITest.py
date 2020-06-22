from graphene.test import Client
from graphene_django.utils import GraphQLTestCase
from graphql_jwt.testcases import JSONWebTokenTestCase

from graphery.schema import schema
from backend.models import *


class GraphQLAPITest(GraphQLTestCase, JSONWebTokenTestCase):
    GRAPHQL_SCHEMA = schema
    fixtures = ['test_data.json', ]

    def test_fixture(self):
        user = User.objects.get(username='default_user')
        self.assertEqual(user.email, 'default@reed.edu')

    def test_tutorial_url_exist(self):
        pass

    def test_tutorial_url_not_exist(self):
        pass

    def test_tutorial_content_trans_exist(self):
        pass

    def test_tutorial_content_trans_not_exist(self):
        pass

    def test_code_exist(self):
        pass

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
