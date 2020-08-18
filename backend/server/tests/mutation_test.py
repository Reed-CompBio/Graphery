import json
from typing import Mapping, Sequence

from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.db import models
from graphene.test import Client

from backend.model.TutorialRelatedModel import FAKE_UUID
from graphery.schema import schema
import pytest

from backend.model.MetaModel import InvitationCode
from backend.models import *
from tests.utils import camel_to_snake, EmptyValue, AnyNoneEmptyValue, AnyValue


@pytest.fixture(autouse=True)
def enable_db_access(db):
    pass


@pytest.fixture()
def rq_anonymous(rf):
    request = rf.post('/')
    SessionMiddleware().process_request(request)
    request.session.save()
    request.user = AnonymousUser()

    return request


@pytest.fixture()
def rq_admin(rf):
    request = rf.post('/')
    SessionMiddleware().process_request(request)
    request.session.save()
    admin = \
        User.objects.create_superuser(username='super_test_user', email='super_test@user.com', password='Password!1')
    request.user = admin

    return request


@pytest.fixture(scope='module')
def graphql_client():
    return Client(schema)


def assert_no_error(result: Mapping) -> Mapping:
    assert 'errors' not in result
    assert 'data' in result
    return result['data']


def assert_model_equal(model_instance: models.Model, variable_mapping: Mapping,
                       validate_against: Mapping = None) -> None:
    for var_name, var_value in {**variable_mapping, **(validate_against if validate_against else {})}.items():
        model_var_value = getattr(model_instance, camel_to_snake(var_name), EmptyValue)
        if isinstance(var_value, Sequence) and all(isinstance(var_value_ele, models.Model) for var_value_ele in var_value):
            assert all(var_value_ele in model_var_value for var_value_ele in var_value)
        else:
            assert var_value == model_var_value


@pytest.mark.parametrize(
    'mutation_query, variables, result_chain, model',
    [
        pytest.param(
            '''mutation ($email: String!, $username: String!, $password: String!, $invitationCode: String!) {
          register(email: $email, username: $username, password: $password, invitationCode:$invitationCode) {
            user {
              id
            }
          }
        }''',
            {'email': 'test_new_register@email.com', 'username': 'test_user_name', 'password': 'Password!1',
             'invitationCode': InvitationCode.code_collection['Visitor']},
            ('register', 'user', 'id'),
            User
        )
    ]
)
def test_register_mutation(graphql_client, rq_anonymous,
                           mutation_query: str, variables: Mapping, result_chain: Sequence, model: models.Model):
    result = graphql_client.execute(mutation_query, variable_values=variables, context_value=rq_anonymous)

    data = assert_no_error(result)

    for chain_id in result_chain:
        data = data.get(chain_id)

    model_instance = model.objects.get(id=data)

    assert_model_equal(model_instance, variables, validate_against={'password': AnyNoneEmptyValue,
                                                                    'invitationCode': AnyValue})


id_validation = {'id': AnyNoneEmptyValue}


@pytest.mark.django_db
@pytest.mark.parametrize(
    'mutation_query, variables, result_chain, model, validate_against',
    [
        pytest.param(
            '''
            mutation($id: UUID!, $category: String!, $isPublished: Boolean) {
              updateCategory(id: $id, category: $category, isPublished: $isPublished) {
                model {
                  id
                }
              }
            }
            ''',
            {'id': FAKE_UUID, 'category': 'Test Mutation Category', 'isPublished': False},
            ('updateCategory', 'model',),
            Category,
            id_validation
        ),
        *(pytest.param(
            '''
            mutation ($id: UUID!, $url: String!, $name: String!, $rank: RankInputType!, $categories: [String], $isPublished: Boolean) {
              updateTutorialAnchor(id: $id, url: $url, name: $name, rank: $rank, categories: $categories, isPublished: $isPublished) {
                success
                model {
                  id
                }
              }
            }
            ''',
            {'id': FAKE_UUID, 'url': url_name_set[0], 'name': url_name_set[1],
             'rank': rank, 'categories': catList, 'isPublished': False},
            ('updateTutorialAnchor', 'model', ),
            Tutorial,
            {**id_validation, 'level': rank['level'], 'section': rank['section'], 'rank': AnyValue, 'categories': AnyValue},
        ) for url_name_set, catList, rank in [
            (('new-test-url-2', 'net test url 2'), [], {'level': 500, 'section': 2}),
            (('new-test-url-1', 'net test url 1'), ['1e209965-f720-418b-8746-1eaee4c8295c', 'dbe8cf6f-09a5-41b6-86ba-367d7a63763f'], {'level': 501, 'section': 2})
        ]),
        *(pytest.param(
            '''
            mutation ($id: UUID!, $url: String!, $name: String!, $cyjs: JSONString!, $isPublished:Boolean, $priority: Int, $authors: [String], $categories: [String], $tutorials: [String]) {
              updateGraph(id: $id, url: $url, name: $name, cyjs: $cyjs, isPublished: $isPublished, priority: $priority, authors: $authors, categories: $categories, tutorials: $tutorials) {
                model {
                  id
                }
              }
            }
            ''',
            {'id': FAKE_UUID, 'url': url_name_set[0], 'name': url_name_set[1],
             'cyjs': json_string, 'priority': 20,
             'categories': catList, 'isPublished': False, 'tutorials': tutList},
            ('updateGraph', 'model', ),
            Graph,
            {**id_validation, 'categories': AnyValue, 'tutorials': AnyValue, 'cyjs': json.loads(json_string)},
        ) for url_name_set, json_string, catList, tutList in [
            (('new-test-url-2', 'net test url 2'), '{"elements": {"edges": [], "nodes": []}, "layout": {"name": "dagre"}}', [], []),
            (('new-test-url-1', 'net test url 1'), '{"elements": {"edges": [], "nodes": []}, "layout": {"name": "preset"}}', ['1e209965-f720-418b-8746-1eaee4c8295c', 'dbe8cf6f-09a5-41b6-86ba-367d7a63763f'], ['7b35ec2c-685f-4727-98c6-766e120fb0c0', '3e8c3a27-bb56-4dd2-92a1-069c26b533e4'])
        ])
    ]
)
def test_admin_mutations_create(graphql_client, rq_admin,
                                mutation_query: str, variables: Mapping, result_chain: Sequence, model: models.Model,
                                validate_against: Mapping):
    result = graphql_client.execute(mutation_query, variable_values=variables, context_value=rq_admin)

    data = assert_no_error(result)

    for result_name in result_chain:
        data = data.get(result_name)

    data_id = data.get('id')

    model_instance = model.objects.get(id=data_id)

    assert_model_equal(model_instance, variables, validate_against=validate_against)
