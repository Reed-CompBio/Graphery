from bundle.GraphObjects.Node import NodeSet
from bundle.GraphObjects.Edge import Edge, EdgeSet
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
