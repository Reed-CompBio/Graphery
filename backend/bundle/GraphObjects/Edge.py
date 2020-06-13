from .Base import Highlightable, Comparable, HasProperty, Stylable, ElementSet
from .Node import Node, NodeSet
from typing import Iterable, Tuple, Mapping


class Edge(Highlightable, Comparable, HasProperty, Stylable):
    _PREFIX = 'e'

    def __init__(self, identity, node_pair: Tuple[Node, Node], name=None, styles=None, classes=None, directed=False):
        Highlightable.__init__(self)
        Comparable.__init__(self, identity, name)
        HasProperty.__init__(self)
        Stylable.__init__(self, styles, classes)
        if isinstance(node_pair, Tuple) and all(isinstance(node, Node) for node in node_pair):
            self.node_pair: Tuple[Node, Node] = node_pair
        else:
            raise KeyError('%s is not a tuple or contains non-node element' % str(node_pair))
        self.directed: bool = directed

    def get_nodes(self) -> Tuple[Node, Node]:
        return self.node_pair

    def get_incident_node(self) -> Node:
        return self.node_pair[0]

    def get_final_node(self) -> Node:
        return self.node_pair[1]

    def is_directed(self) -> bool:
        return self.directed

    def highlight(self, cls: str):
        raise NotImplementedError

    def unhighlight(self, cls: str):
        raise NotImplementedError

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.identity == other.identity and self.node_pair == other.node_pair
        return False

    def __contains__(self, item):
        if isinstance(item, Node):
            return item in self.node_pair
        return False

    def __iter__(self):
        for node in self.node_pair:
            yield node

    def __len__(self):
        return 2

    def __str__(self):
        return str(self.node_pair)

    def __repr__(self):
        return self.__str__()


class EdgeSet(ElementSet[Edge]):
    def __init__(self, edges: Iterable[Edge]):
        super(EdgeSet, self).__init__(edges, Edge)

    @staticmethod
    def generate_edge_set(edges: Iterable[Mapping], nodes: NodeSet) -> 'EdgeSet':
        stored_edges = []
        for edge in edges:
            if isinstance(edge, Mapping) and 'data' in edge and 'id' in edge['data']:
                data_field = edge['data']
                stored_edge = Edge(data_field['id'], (nodes[data_field['source']], nodes[data_field['target']]))
                if 'displayed' in data_field:
                    stored_edge.update_properties(data_field['displayed'])
                stored_edges.append(stored_edge)
            else:
                raise ValueError('invalid format for Edge')

        return EdgeSet(stored_edges)
