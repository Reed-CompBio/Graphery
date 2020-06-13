import pytest
from bundle.GraphObjects.Graph import Graph
from bundle.GraphObjects.Node import Node
from bundle.GraphObjects.Edge import Edge
from .utils import path_join, TEST_PATH


@pytest.fixture()
def simple_graph_js():
    with open(path_join(TEST_PATH, 'test_files', 'graphs', 'simple_graph.cyjs'), 'r') as file:
        return file.read()


def test_simple_graph_parsing(simple_graph_js):
    simple_graph = Graph.graph_generator(simple_graph_js)

    assert len(simple_graph.edge_set) == 16
    
    assert Edge(0, (Node('n0'), Node('n1'))) in simple_graph
    assert Edge(1, (Node('n1'), Node('n2'))) in simple_graph
    assert Edge(2, (Node('n1'), Node('n3'))) in simple_graph
    assert Edge(3, (Node('n2'), Node('n7'))) in simple_graph
    assert Edge(4, (Node('n2'), Node('n11'))) in simple_graph
    assert Edge(5, (Node('n3'), Node('n4'))) in simple_graph
    assert Edge(6, (Node('n3'), Node('n16'))) in simple_graph
    assert Edge(7, (Node('n4'), Node('n5'))) in simple_graph
    assert Edge(8, (Node('n4'), Node('n6'))) in simple_graph
    assert Edge(9, (Node('n6'), Node('n8'))) in simple_graph
    assert Edge(10, (Node('n8'), Node('n9'))) in simple_graph
    assert Edge(11, (Node('n8'), Node('n10'))) in simple_graph
    assert Edge(12, (Node('n11'), Node('n12'))) in simple_graph
    assert Edge(13, (Node('n12'), Node('n13'))) in simple_graph
    assert Edge(14, (Node('n13'), Node('n14'))) in simple_graph
    assert Edge(15, (Node('n13'), Node('n15'))) in simple_graph

    assert len(simple_graph.node_set) == 17

    for i in range(17):
        assert Node('n%d' % i) in simple_graph

