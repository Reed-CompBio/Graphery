import logging

from .Base import Highlightable, Comparable, HasProperty, Stylable, ElementSet
from typing import Iterable, Mapping


class Node(Highlightable, Comparable, HasProperty, Stylable):
    def __init__(self, identity, name=None, styles=None, classes=None):
        Comparable.__init__(self, identity, name)
        HasProperty.__init__(self)
        Stylable.__init__(self, styles, classes)

    def highlight(self, cls):
        # TODO
        raise NotImplementedError

    def unhighlight(self, cls):
        # TODO
        raise NotImplementedError

    def __str__(self):
        return 'Node(id: %s)' % self.identity

    def __repr__(self):
        return self.__str__()


class NodeSet(ElementSet[Node]):
    def __init__(self, nodes: Iterable[Node]):
        super(NodeSet, self).__init__(nodes, Node)

    @staticmethod
    def generate_node_set(nodes: Iterable[Mapping]) -> 'NodeSet':
        stored_nodes = []
        for node in nodes:
            if isinstance(node, Mapping) and 'data' in node and 'id' in node['data']:
                data_field = node['data']
                stored_node = Node(data_field['id'])
                if 'displayed' in data_field:
                    stored_node.update_properties(data_field['displayed'])
            else:
                logging.warning('Omitted one node info since does not contain valid data')

        return NodeSet(stored_nodes)
