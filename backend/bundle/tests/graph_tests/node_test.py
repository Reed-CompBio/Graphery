import pytest
from bundle.GraphObjects.Node import Node, NodeSet
import json
from .utils import TEST_PATH, path_join


@pytest.fixture()
def node_json_obj():
    with open(path_join(TEST_PATH, 'test_files', 'nodes', 'nodes.json')) as file:
        string = file.read()
        return json.loads(string)


@pytest.fixture()
def single_node(node_json_obj):
    return node_json_obj['single_node']


@pytest.fixture()
def multiple_nodes(node_json_obj):
    return node_json_obj['multiple_nodes']


@pytest.fixture()
def complex_node(node_json_obj):
    return node_json_obj['complex_node']


@pytest.fixture()
def complex_nodes(node_json_obj):
    return node_json_obj['node_json_obj']


def test_empty_iter_node_set():
    node_set = NodeSet.generate_node_set([])
    assert str(node_set) == '[]'


def test_none_node_set():
    with pytest.raises(TypeError, match="'NoneType' object is not iterable"):
        node_set = NodeSet.generate_node_set(None)


def test_single_node(single_node):
    node_set = Node(single_node[0]['data']['id'])
    assert str(node_set) == 'Node(id: n1)'


def test_single_node_set(single_node):
    node_set = NodeSet.generate_node_set(single_node)
    assert str(node_set) == '[Node(id: n1)]'


def test_multiple_node_set(multiple_nodes):
    node_set = NodeSet.generate_node_set(multiple_nodes)
    assert str(node_set) == '[Node(id: n1), Node(id: n2), Node(id: n3)]'


def test_complex_node_set(complex_node):
    node_set = NodeSet.generate_node_set(complex_node)
    assert node_set.elements[0].properties == {"degree": 0, "clustering_coefficient": 0}

