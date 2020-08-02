from bundle.seeker import tracer
from bundle.utils.dummy_graph import graph_object


@tracer('node')
def main() -> None:
    for node in graph_object.V:
        print(node)
