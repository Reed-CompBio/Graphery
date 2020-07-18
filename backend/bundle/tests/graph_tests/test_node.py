import pytest
from bundle.GraphObjects.Node import Node, NodeSet, MutableNodeSet
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
        # noinspection PyTypeChecker
        NodeSet.generate_node_set(None)


def test_single_node(single_node):
    node_set = Node(single_node[0]['data']['id'])
    assert str(node_set) == 'Node(id: n1)'


def test_single_node_set(single_node):
    node_set = NodeSet.generate_node_set(single_node)
    assert str(node_set) == '[Node(id: n1)]'


def test_multiple_node_set(multiple_nodes):
    node_set = NodeSet.generate_node_set(multiple_nodes)
    assert len(node_set) == 3
    assert Node('n1') in node_set
    assert Node('n2') in node_set
    assert Node('n3') in node_set


def test_complex_node_set(complex_node):
    node_set = NodeSet.generate_node_set(complex_node)
    assert node_set.elements[0].properties == {"degree": 0, "clustering_coefficient": 0}


@pytest.fixture
def mutable_node_set():
    return MutableNodeSet()


def test_mutable_node_set_add_node(mutable_node_set: MutableNodeSet):
    node1 = Node('1')
    mutable_node_set.add_node(node1)

    assert node1 in mutable_node_set
    assert not mutable_node_set.is_empty()


def test_duplicate_nodes(mutable_node_set: MutableNodeSet):
    node1 = Node('1')

    mutable_node_set.add_node(node1)
    mutable_node_set.add_node(node1)

    assert node1 in mutable_node_set
    assert len(mutable_node_set) == 1


def test_mutable_node_set_add_nodes(mutable_node_set: MutableNodeSet):
    node_list = []

    for i in range(10):
        node_list.append(Node(f'{i}'))

    mutable_node_set.add_node(*node_list)

    assert all(node in mutable_node_set for node in node_list)
    assert len(mutable_node_set) == len(node_list)


def test_mutable_node_set_remove_node(mutable_node_set):
    node1 = Node('1')
    mutable_node_set.add_node(node1)
    mutable_node_set.remove_node(node1)

    assert node1 not in mutable_node_set
    assert mutable_node_set.is_empty()


def test_mutable_node_set_remove_nodes(mutable_node_set):
    node_list = []

    for i in range(10):
        node_list.append(Node(f'{i}'))

    mutable_node_set.add_node(*node_list)
    mutable_node_set.remove_node(*node_list)

    assert all(node not in mutable_node_set for node in node_list)
    assert mutable_node_set.is_empty()
