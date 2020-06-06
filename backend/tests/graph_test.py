import pytest
from GraphObjects.Graph import Graph


@pytest.fixture()
def simple_graph_js():
    with open('test_files/graphs/simple_graph.cyjs', 'r') as file:
        return file.read()


def test_simple_graph_parsing(simple_graph_js):
    simple_graph = Graph.graph_generator(simple_graph_js)
