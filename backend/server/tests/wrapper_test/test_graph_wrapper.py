from uuid import UUID

import pytest

from backend.intel_wrappers.intel_wrapper import GraphWrapper
from backend.intel_wrappers.validators import ValidationError
from backend.model.TutorialRelatedModel import GraphPriority
from tests.wrapper_test.factories import category_wrappers_factory, user_wrappers_factory, \
    tutorial_anchor_wrappers_factory
from tests.wrapper_test.test_wrapper_helper import gen_wrapper_test_class


# for pycharm quick start
class TestGraphWrapper:
    def test_func(self):
        pass


# noinspection PyRedeclaration
TestGraphWrapper = gen_wrapper_test_class(wrapper_class=GraphWrapper, test_params={
    'test_load': [
        pytest.param('stored_mock_graph', True),
        pytest.param('stored_mock_graph', False)
    ],
    'test_set_variables': [
        pytest.param({
            'url': 'test-set-var-graph',
            'name': 'test set var graph',
            'categories': category_wrappers_factory('graph wrapper set var {}', 1),
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': False
        }),
        pytest.param({
            'url': 'test-set-var-graph',
            'name': 'test set var graph',
            'categories': category_wrappers_factory('graph wrapper set var {}', 10),
            'authors': user_wrappers_factory(
                username_template='graph_user_{}', email_template='graph_user_{}@graph.com', num=10
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
                url_template='graph-tutorial-url-{}', name_template='graph tutorial {}', num=10
            ),
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': False
        }),
        pytest.param({
            'categories': category_wrappers_factory('graph wrapper set var {}', 10),
            'authors': user_wrappers_factory(
                username_template='graph_user_{}', email_template='graph_user_{}@graph.com', num=10
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
                url_template='graph-tutorial-url-{}', name_template='graph tutorial {}', num=10
            ),
        }),
        {
            'categories': category_wrappers_factory('graph wrapper set var {}', 0),
            'authors': user_wrappers_factory(
                username_template='graph_user_{}', email_template='graph_user_{}@graph.com', num=0
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
                url_template='graph-tutorial-url-{}', name_template='graph tutorial {}', num=0
            ),
        },
        {
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'}
        },
        {
            'url': 'test-set-var-graph',
            'name': 'test set var graph',
        },
        {
            'url': 'test-set-var',
            'name': 'test set var',
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'}
        },
        {

        }
    ],
    'test_making_new_model': [
        pytest.param({
            'url': 'test-set-var-graph',
            'name': 'test set var graph',
            'categories': category_wrappers_factory('graph wrapper set var {}', 7),
            'authors': user_wrappers_factory(
                username_template='graph_user_{}', email_template='graph_user_{}@graph.com', num=5
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
                url_template='graph-tutorial-url-{}', name_template='graph tutorial {}', num=0
            ),
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': False
        }),
        pytest.param({
            'url': 'test-set-var-graph',
            'name': 'test set var graph',
            'categories': None,
            'authors': None,
            'tutorials': None,
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': False
        }),
    ],
    'test_retrieve_model': [
        pytest.param('stored_mock_graph', {'id': UUID('6a831c16-903d-47d8-94ac-61d8bd419bd3'), })
    ],
    'test_overwrite': [
        pytest.param('one_time_mock_graph', {
            'url': 'one-time-mock-test-graph-mod',
            'name': 'one time mock test graph mod',
            'categories': category_wrappers_factory('test overwrite {}', 5),
            'authors': user_wrappers_factory(
                username_template='graph_user_{}', email_template='graph_user_{}@graph.com', num=5
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
                url_template='graph-tutorial-url-{}', name_template='graph tutorial {}', num=0
            ),
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': False
        }),
        pytest.param('one_time_mock_graph', {
            'url': 'one-time-mock-test-graph-mod',
            'name': 'one time mock test graph mod',
            'categories': category_wrappers_factory('test overwrite {}', 0),
            'authors': user_wrappers_factory(
                username_template='graph_user_{}', email_template='graph_user_{}@graph.com', num=0
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
                url_template='graph-tutorial-url-{}', name_template='graph tutorial {}', num=0
            ),
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': False
        }),
        pytest.param('one_time_mock_graph', {
            'categories': category_wrappers_factory('test overwrite {}', 0),
            'authors': user_wrappers_factory(
                username_template='graph_user_{}', email_template='graph_user_{}@graph.com', num=9
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
                url_template='graph-tutorial-url-{}', name_template='graph tutorial {}', num=8
            ),
        }),
        pytest.param('one_time_mock_graph', {
            'priority': GraphPriority.MAIN,
            'cyjs': {'json': 'hello'},
            'is_published': False
        }),
        pytest.param('one_time_mock_graph', {
            'url': 'one-time-mock-test-graph-mod',
            'name': 'one time mock test graph mod',
            'is_published': True
        }),
        pytest.param('one_time_mock_graph', {

        }
                     )
    ],
    'test_validation': [
        pytest.param({'url': ''}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': ''}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': None}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': [], 'authors': None}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': [], 'authors': [], 'tutorials': None}, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': [], 'authors': [], 'tutorials': [], }, ValidationError,
                     None),
        pytest.param({'url': 't', 'name': '', 'categories': [], 'authors': [], 'tutorials': [], 'priority': 500000, },
                     ValidationError,
                     None),
        pytest.param(
            {'url': 't', 'name': '', 'categories': [], 'authors': [], 'tutorials': [], 'priority': GraphPriority.MAIN,
             'cyjs': object()}, ValidationError,
            None),
    ],
    'test_get_model': [
        pytest.param(None, {
            'url': 'one-time-mock-test-graph-mod',
            'name': 'one time mock test graph mode',
            'priority': GraphPriority.MAIN,
            'cyjs': {},
            'is_published': False
        }, False, False, AssertionError, 'Cannot make new model without validations!'),
        pytest.param(None, {
            'url': 'one-time-mock-test-graph-mod',
            'name': 'one time mock test graph mode',
            'priority': GraphPriority.MAIN,
            'cyjs': {},
            'categories': [],
            'authors': [],
            'tutorials': [],
            'is_published': False
        }, True, True, None, None, id='make new model'),
        pytest.param('stored_mock_graph', {
            'id': UUID('6a831c16-903d-47d8-94ac-61d8bd419bd3'),
            'url': 'one-time-mock-test-graph-mod',
            'name': 'one time mock test graph mode',
            'priority': GraphPriority.MAIN,
            'cyjs': {},
            'categories': [],
            'authors': [],
            'tutorials': [],
            'is_published': False
        }, True, False, None, None, id='get old model')
    ],
    'test_finalize': [
        pytest.param('one_time_mock_graph', {
            'url': 'finalize-test-graph',
            'name': 'finalize test graph',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'authors': user_wrappers_factory(
                username_template='full-mod-finalize-user-{}', email_template='mod-user-{}@user.com', num=10
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
              url_template='full-mod-graph-t-{}',
              name_template='full mod graph t {}',
              num=9
            ),
            'priority': GraphPriority.SUPP,
            'cyjs': {'json': 'hello world'},
            'is_published': False
        }, True, True, None, None),
        pytest.param('one_time_mock_graph', {
            'url': 'finalize-test-graph',
            'name': 'finalize test graph',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'authors': user_wrappers_factory(
                username_template='full-mod-finalize-user-{}', email_template='mod-user-{}@user.com', num=10
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
              url_template='full-mod-graph-t-{}',
              name_template='full mod graph t {}',
              num=6
            ),
            'priority': GraphPriority.SUPP,
            'cyjs': {'json': 'hello world'},
            'is_published': False
        }, True, False, None, None),
        pytest.param('one_time_mock_graph', {
            'url': 'finalize-test-graph',
            'name': 'finalize test graph',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'authors': user_wrappers_factory(
                username_template='full-mod-finalize-user-{}', email_template='mod-user-{}@user.com', num=0
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
              url_template='full-mod-graph-t-{}',
              name_template='full mod graph t {}',
              num=0
            ),
        }, True, True, None, None),
        pytest.param('one_time_mock_graph', {
            'url': ''
        }, True, True, ValidationError, None),
        pytest.param(None, {
            'url': 'finalize-test-graph',
            'name': 'finalize test graph',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'authors': user_wrappers_factory(
                username_template='full-mod-finalize-user-{}', email_template='mod-user-{}@user.com', num=10
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
              url_template='full-mod-graph-t-{}',
              name_template='full mod graph t {}',
              num=2
            ),
            'priority': GraphPriority.SUPP,
            'cyjs': {'json': 'hello world'},
            'is_published': True
        }, True, True, None, None),
        pytest.param(None, {
            'url': 'finalize-test-empty-graph',
            'name': 'finalize test empty graph',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'authors': user_wrappers_factory(
                username_template='full-mod-finalize-user-{}', email_template='mod-user-{}@user.com', num=2
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
              url_template='full-mod-graph-t-{}',
              name_template='full mod graph t {}',
              num=3
            ),
            'priority': GraphPriority.SUPP,
            'cyjs': {'json': 'hello world'},
            'is_published': True
        }, True, True, None, None),
        pytest.param(None, {
            'url': 'finalize-test-graph',
            'name': 'finalize test graph',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'authors': user_wrappers_factory(
                username_template='full-mod-finalize-user-{}', email_template='mod-user-{}@user.com', num=5
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
              url_template='full-mod-graph-t-{}',
              name_template='full mod graph t {}',
              num=7
            ),
            'priority': GraphPriority.SUPP,
            'cyjs': {'json': 'hello world'},
            'is_published': False
        }, False, True, AssertionError, None),
        pytest.param(None, {
            'url': 'finalize-test-graph',
            'name': 'finalize test graph',
            'categories': category_wrappers_factory('full mod finalize {}', 5),
            'authors': user_wrappers_factory(
                username_template='full-mod-finalize-user-{}', email_template='mod-user-{}@user.com', num=10
            ),
            'tutorials': tutorial_anchor_wrappers_factory(
              url_template='full-mod-graph-t-{}',
              name_template='full mod graph t {}',
              num=1
            ),
            'priority': GraphPriority.SUPP,
            'cyjs': {'json': 'hello world'},
            'is_published': False
        }, True, False, AssertionError, None),
    ]
}, default_params={'is_published': False})
