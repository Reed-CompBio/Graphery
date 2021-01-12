import pytest
from bundle.GraphObjects.Graph import Graph, MutableGraph, GraphLayout
from bundle.GraphObjects.Node import Node
from bundle.GraphObjects.Edge import Edge
from .utils import path_join, TEST_PATH


@pytest.fixture()
def simple_graph_js():
    with open(path_join(TEST_PATH, 'test_files', 'graphs', 'simple_graph.cyjs')) as file:
        return file.read()


def test_simple_graph_parsing(simple_graph_js):
    simple_graph = Graph.graph_generator(simple_graph_js)

    assert len(simple_graph.edges) == 16
    
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

    assert GraphLayout.fcose.value == simple_graph.layout

    assert len(simple_graph.nodes) == 17

    for i in range(17):
        assert Node('n%d' % i) in simple_graph


@pytest.fixture
def mutable_graph():
    return MutableGraph()


def test_mutable_graph_add_node(mutable_graph: MutableGraph):
    mutable_graph.add_node('1')
    assert Node('1') in mutable_graph
    assert len(mutable_graph.V) == 1


def test_mutable_graph_add_edge(mutable_graph: MutableGraph):
    mutable_graph.add_edge('1', ('n1', 'n2'))
    assert Edge('1', (Node('n1'), Node('n2'))) in mutable_graph
    assert len(mutable_graph.E) == 1


def test_mutable_graph_delete_node_no_conflict(mutable_graph: MutableGraph):
    node_num = 20

    edge_list = []
    for i in range(node_num // 2):
        node = mutable_graph.add_node(f'{i}')
        node_ = mutable_graph.add_node(f'{i}_{i}')
        edge_list.append(mutable_graph.add_edge(edge=Edge(i, (node_, node))))

    common_node = mutable_graph.add_node('11')

    assert all(edge in mutable_graph.E for edge in edge_list)
    assert all(all(node in mutable_graph.V for node in edge) for edge in edge_list)
    assert common_node in mutable_graph.V
    assert len(edge_list) == len(mutable_graph.E)
    assert len(mutable_graph.V) == node_num + 1

    mutable_graph.remove_node(common_node)

    assert len(edge_list) == len(mutable_graph.E)
    assert all(edge in mutable_graph.E for edge in edge_list)
    assert all(all(node in mutable_graph.V for node in edge) for edge in edge_list)
    assert common_node not in mutable_graph.V
    assert len(mutable_graph.V) == node_num


def test_mutable_graph_delete_node_conflict_delete_nothing(mutable_graph: MutableGraph):
    last_num = 10
    common_node = Node(f'{last_num}')
    mutable_graph.add_node(common_node)

    edge_list = []
    for i in range(last_num):
        node = mutable_graph.add_node(f'{i}')
        edge_list.append(mutable_graph.add_edge(edge=Edge(i, (common_node, node))))

    assert len(edge_list) == len(mutable_graph.E)
    assert len(mutable_graph.V) == last_num + 1
    assert common_node in mutable_graph.V
    assert all(edge in mutable_graph.E for edge in edge_list)
    assert all(all(node in mutable_graph.V for node in edge) for edge in edge_list)

    mutable_graph.remove_node(common_node)

    assert len(edge_list) == len(mutable_graph.E)
    assert len(mutable_graph.V) == last_num + 1
    assert all(edge in mutable_graph.E for edge in edge_list)
    assert all(all(node in mutable_graph.V for node in edge) for edge in edge_list)
    assert common_node in mutable_graph.V


def test_mutable_graph_delete_node_conflict_delete_anything(mutable_graph: MutableGraph):
    last_num = 10
    common_node = mutable_graph.add_node(f'{last_num}')

    edge_list = []
    for i in range(last_num):
        node = mutable_graph.add_node(f'{i}')
        edge_list.append(mutable_graph.add_edge(edge=Edge(i, (common_node, node))))

    assert all(edge in mutable_graph.E for edge in edge_list)
    assert all(all(node in mutable_graph.V for node in edge) for edge in edge_list)
    assert len(edge_list) == len(mutable_graph.E)
    assert len(mutable_graph.V) == last_num + 1
    assert common_node in mutable_graph.V

    mutable_graph.remove_node(common_node, True)

    assert len(mutable_graph.E) == 0
    assert len(mutable_graph.V) == last_num
    assert common_node not in mutable_graph.V
    assert all(edge not in mutable_graph.E for edge in edge_list)
    assert all(edge.node_pair[1] in mutable_graph.V for edge in edge_list)


def test_mutable_graph_delete_edge(mutable_graph: MutableGraph):
    node1 = mutable_graph.add_node('1')
    node2 = mutable_graph.add_node('2')
    edge = mutable_graph.add_edge('3', (node1, node2))

    assert edge in mutable_graph
    assert node1 in mutable_graph
    assert node2 in mutable_graph

    mutable_graph.remove_edge(edge)

    assert edge not in mutable_graph
    assert node1 in mutable_graph
    assert node2 in mutable_graph


def test_mutable_graph_generate_json():
    pass
