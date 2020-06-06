from .Base import Highlightable, Comparable, HasProperty, Stylable, ElementSet
from .Node import Node
from typing import Iterable, Tuple


class Edge(Highlightable, Comparable, HasProperty, Stylable):
    def __init__(self, identity, node_pair: Tuple[Node, Node] = None, name=None, styles=None, classes=None, directed=False):
        Highlightable.__init__(self)
        Comparable.__init__(self, identity, name)
        HasProperty.__init__(self)
        Stylable.__init__(self, styles, classes)
        if isinstance(node_pair, Tuple) and all(isinstance(node, Node) for node in node_pair):
            self.edge = tuple(node_pair)
        else:
            raise KeyError
        self.directed = directed

    def get_nodes(self) -> Tuple[Node, Node]:
        return self.edge

    def get_incident_node(self) -> Node:
        return self.edge[0]

    def get_final_node(self) -> Node:
        return self.edge[1]

    def is_directed(self) -> bool:
        return self.directed

    def highlight(self, cls: str):
        raise NotImplementedError

    def unhighlight(self, cls: str):
        raise NotImplementedError


class EdgeSet(ElementSet):
    def __init__(self, edges: Iterable[Edge]):
        super(EdgeSet, self).__init__(edges, Edge)
