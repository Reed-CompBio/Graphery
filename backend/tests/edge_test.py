from GraphObjects.Node import NodeSet
from GraphObjects.Edge import Edge, EdgeSet
from .utils import TEST_PATH, path_join
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


def test_multiple_edges(multiple_edges):
    node_set = NodeSet.generate_node_set(multiple_edges['nodes'])
    edge_set = EdgeSet.generate_edge_set(multiple_edges['edges'], node_set)
    assert str(edge_set) == '[(Node(id: n0), Node(id: n1)), (Node(id: n1), Node(id: n2)), ' \
                            '(Node(id: n1), Node(id: n3)), (Node(id: n3), Node(id: n4)), ' \
                            '(Node(id: n4), Node(id: n5)), (Node(id: n4), Node(id: n6))]'
