from bundle.seeker import tracer
from bundle.utils.dummy_graph import graph_object


@tracer('edge')
def main() -> None:
    for edge in graph_object.V:
        print(edge)
