from .Base import Comparable, HasProperty, Stylable, ElementSet
from .Errors import GraphJsonFormatError
from .Node import Node, NodeSet
from typing import Iterable, Tuple, Mapping, Union
from collections import namedtuple

NodeTuple = namedtuple('Edge', ('u', 'v'))
EdgeIDTuple = namedtuple('edge_identities', ('incident_edge_identity', 'final_edge_identity'))


class Edge(Comparable, HasProperty, Stylable):
    _PREFIX = 'e'

    def __init__(self, identity, node_pair: NodeTuple, name=None,
                 styles: Iterable[Mapping] = (), classes: Iterable[str] = (), directed=False):
        """
        create an edge with an identity and a pair of nodes
        @param identity:
        @param node_pair:
        @param name:
        @param styles: the styles used on this edge
        @param classes: the class used on this edge
        @param directed: whether this edge is directed
        @raise KeyError: if there is some problem with the node pair
        """
        Comparable.__init__(self, identity, name)
        HasProperty.__init__(self)
        Stylable.__init__(self, styles, classes)
        if isinstance(node_pair, Tuple) and all(isinstance(node, Node) for node in node_pair):
            self.node_pair: NodeTuple = node_pair
        else:
            raise KeyError('%s is not a tuple or contains non-node element' % str(node_pair))
        self.directed: bool = directed

    def get_nodes(self) -> Tuple[Node, Node]:
        """
        get the node pairs in this edge
        @return:
        """
        return self.node_pair

    def get_incident_node(self) -> Node:
        """
        get the incident node in this pair, which is always the first element in the tuple
        @return:
        """
        return self.node_pair[0]

    def get_final_node(self) -> Node:
        """
        get the final node in this pair, which is always the second element in the tuple
        @return:
        """
        return self.node_pair[1]

    def is_directed(self) -> bool:
        """
        show whether the edge is directed or not
        @return:
        """
        return self.directed

    def reverse_direction(self) -> None:
        """
        change the direction if the edge is directed
        @return:
        """
        if self.is_directed():
            self.node_pair = self.node_pair[::-1]

    def __contains__(self, node):
        """
        returns true if a node is part of this edge
        @param node:
        @return:
        """
        if isinstance(node, Node):
            return node in self.node_pair
        return False

    def __iter__(self):
        """
        iterator that goes through the nodes in this edge
        @return:
        """
        for node in self.node_pair:
            yield node

    def __len__(self):
        """
        something that does not make sense
        @return:
        """
        return 2

    def __str__(self):
        return str(self.node_pair)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def return_edge(identity: str = None, edge: Union['Edge', NodeTuple, Tuple[str, str]] = (),
                    styles: Iterable[Mapping] = (), classes: Iterable[str] = ()) -> 'Edge':

        if isinstance(identity, str):
            if isinstance(edge, NodeTuple):
                incident_node, final_node = edge
            elif isinstance(edge, Tuple) and all(isinstance(ele, (str, Node)) for ele in edge):
                incident_node, final_node = Node.return_node(edge[0]), Node.return_node(edge[1])
            else:
                # TODO think about it
                incident_node, final_node = None, None
            return Edge(identity, NodeTuple(incident_node, final_node), styles, classes)
        else:
            if isinstance(edge, Edge):
                return edge
            else:
                raise TypeError('The edge must be a edge if the identity is not a string')


class EdgeSet(ElementSet):
    def __init__(self, edges: Iterable[Edge]):
        """
        Create an edge set with a pile of elements.
        @param edges:
        """
        super(EdgeSet, self).__init__(edges, Edge)

    @staticmethod
    def generate_edge_set(edges: Iterable[Mapping], nodes: NodeSet) -> 'EdgeSet':
        """
        generate an edge set by a given mapping (from cyjs) and the corresponding nodes
        @param edges:
        @param nodes:
        @return: created edge set
        @raise ValueError: if the data is invalid
        """
        stored_edges = []
        for edge in edges:
            if not (isinstance(edge, Mapping) and 'data' in edge):
                raise GraphJsonFormatError(f'invalid format for Edge {edge}')

            data_field = edge['data']

            if not ('id' in data_field and 'source' in data_field and 'target' in data_field):
                raise GraphJsonFormatError(f'The edge {edge} entry must contain `id`, `source` and `target` fields')

            stored_edge = Edge(data_field['id'], NodeTuple(nodes[data_field['source']], nodes[data_field['target']]))
            if 'displayed' in data_field:
                stored_edge.update_properties(data_field['displayed'])
            stored_edges.append(stored_edge)

        return EdgeSet(stored_edges)


class MutableEdgeSet(EdgeSet):
    def __init__(self, edges: Iterable[Edge] = ()):
        super(MutableEdgeSet, self).__init__(edges)

    def add_edge(self, *edges: Edge) -> None:
        if not all(isinstance(edge, self.element_type) for edge in edges):
            raise TypeError(f'Mutable Edge Set only accepts {self.element_type}')

        self.elements.update(edges)

    def remove_edge(self, *edges: Edge) -> None:
        if not all(isinstance(edge, self.element_type) for edge in edges):
            raise TypeError(f'Mutable Edge Set only accepts {self.element_type}')

        for edge in edges:
            self.elements.remove(edge)
