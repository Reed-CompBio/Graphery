import re
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
def test_client():
    return Client(schema)


class EmptyVal:
    pass


def camel_to_snake(var_name: str) -> str:
    var_name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', var_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', var_name).lower()


def assert_no_error(result: Mapping) -> Mapping:
    assert 'errors' not in result
    assert 'data' in result
    return result['data']


def assert_model_equal(model_instance: models.Model, variable_mapping: Mapping, exclude_list: Sequence = ()) -> None:
    for var_name, var_value in variable_mapping.items():
        if var_name in exclude_list:
            continue
        model_var_value = getattr(model_instance, camel_to_snake(var_name), EmptyVal)
        assert model_var_value == var_value


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
def test_register_mutation(test_client, rq_anonymous,
                           mutation_query: str, variables: Mapping, result_chain: Sequence, model: models.Model):
    result = test_client.execute(mutation_query, variable_values=variables, context_value=rq_anonymous)

    data = assert_no_error(result)

    for chain_id in result_chain:
        data = data.get(chain_id)

    model_instance = model.objects.get(id=data)

    assert_model_equal(model_instance, variables, exclude_list=('password', 'invitationCode'))


id_exclude_list = ('id',)


@pytest.mark.parametrize(
    'mutation_query, variables, result_chain, model, exclude_list',
    [
        pytest.param(
            '''mutation($id: UUID!, $category: String!, $isPublished: Boolean) {
                  updateCategory(id: $id, category: $category, isPublished: $isPublished) {
                    model {
                      id
                    }
                  }
                }
            ''',
            {'id': FAKE_UUID, 'category': 'Test Mutation Category', 'isPublished': True},
            ('updateCategory', 'model',),
            Category,
            id_exclude_list
        )
    ]
)
def test_admin_mutations_create(test_client, rq_admin,
                                mutation_query: str, variables: Mapping, result_chain: Sequence, model: models.Model,
                                exclude_list: Sequence):
    result = test_client.execute(mutation_query, variable_values=variables, context_value=rq_admin)

    data = assert_no_error(result)

    for result_name in result_chain:
        data = data.get(result_name)

    data_id = data.get('id')

    model_instance = model.objects.get(id=data_id)

    assert_model_equal(model_instance, variables, exclude_list=exclude_list)
