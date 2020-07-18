from bundle.GraphObjects.Node import NodeSet, Node
from bundle.GraphObjects.Edge import Edge, EdgeSet, MutableEdgeSet
from .utils import TEST_PATH, path_join, gen_edge
import pytest
import json


@pytest.fixture()
def edge_json_obj():
    with open(path_join(TEST_PATH, 'test_files', 'edges', 'edges.json'), 'r') as file:
        string = file.read()
        return json.loads(string)


@pytest.fixture()
def multiple_edges(edge_json_obj):
    return edge_json_obj['multiple_edges']


@pytest.mark.parametrize('expected', [
    [(1, 0, 1), (2, 1, 2), (3, 1, 3), (4, 3, 4), (5, 4, 5), (6, 4, 6)]
])
def test_multiple_edges(multiple_edges, expected):
    node_set = NodeSet.generate_node_set(multiple_edges['nodes'])
    edge_set = EdgeSet.generate_edge_set(multiple_edges['edges'], node_set)
    assert len(edge_set) == 6
    for test_set in expected:
        assert gen_edge(test_set[0], 'n%s' % test_set[1], 'n%s' % test_set[2]) in edge_set


@pytest.fixture
def mutable_edge_set():
    return MutableEdgeSet()


def test_mutable_edge_set_add_edge(mutable_edge_set):
    node1 = Node('1')
    node2 = Node('2')
    edge = Edge('e1', (node1, node2))
    mutable_edge_set.add_edge(edge)

    assert edge in mutable_edge_set
    assert not mutable_edge_set.is_empty()


def test_mutable_edge_set_remove_edge(mutable_edge_set):
    node1 = Node('1')
    node2 = Node('2')
    edge = Edge('e1', (node1, node2))
    mutable_edge_set.add_edge(edge)
    mutable_edge_set.remove_edge(edge)

    assert edge not in mutable_edge_set
    assert mutable_edge_set.is_empty()
