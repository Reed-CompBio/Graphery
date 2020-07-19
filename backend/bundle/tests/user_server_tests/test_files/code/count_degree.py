from bundle.seeker import tracer
from bundle.utils.dummy_graph import graph_object


@tracer('node', 'node_degree', 'edge', 'degree_dict')
def main() -> None:
    degree_dict = {}
    for node in graph_object.V:
        node_degree = 0
        for edge in graph_object.edges:
            if node in edge:
                node_degree += 1
        degree_dict[node] = node_degree
