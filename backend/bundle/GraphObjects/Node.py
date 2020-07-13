from .Base import Comparable, HasProperty, Stylable, ElementSet
from typing import Iterable, Mapping

from .Errors import GraphJsonFormatError


class Node(Comparable, HasProperty, Stylable):
    _PREFIX = 'v'

    def __init__(self, identity, name=None, styles=None, classes=None):
        """
        create an node with an identity
        @param identity:
        @param name:
        @param styles: the styles applied to this node
        @param classes: the classes applied to this node
        """
        Comparable.__init__(self, identity, name)
        HasProperty.__init__(self)
        Stylable.__init__(self, styles, classes)

    def __str__(self):
        return 'Node(id: %s)' % self.identity

    def __repr__(self):
        return self.__str__()


class NodeSet(ElementSet):
    def __init__(self, nodes: Iterable[Node]):
        """
        Create an edge set with a pile of elements.
        @param nodes:
        """
        super(NodeSet, self).__init__(nodes, Node)

    @staticmethod
    def generate_node_set(nodes: Iterable[Mapping]) -> 'NodeSet':
        stored_nodes = []
        for node in nodes:
            if not (isinstance(node, Mapping) and 'data' in node and 'id' in node['data']):
                raise GraphJsonFormatError(f'invalid format for Node {node}')

            data_field = node['data']
            if not ('id' in data_field):
                raise GraphJsonFormatError(f'The node {node} entry must contain a `id` field')

            stored_node = Node(data_field['id'])
            if 'displayed' in data_field:
                stored_node.update_properties(data_field['displayed'])
            stored_nodes.append(stored_node)

        return NodeSet(stored_nodes)
