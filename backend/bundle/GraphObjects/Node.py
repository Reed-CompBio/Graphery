from __future__ import annotations

import warnings

from .Base import Comparable, HasProperty, Stylable, ElementSet
from typing import Iterable, Mapping, Union, Tuple

from .Errors import GraphJsonFormatError


class Node(Comparable, HasProperty, Stylable):
    _PREFIX = 'v'

    def __init__(self, identity: str, name: str = None,
                 styles: Union[str, Iterable[Mapping]] = (), classes: Iterable[str] = (),
                 add_default_styles=False, add_default_classes=False):
        """
        create an node with an identity
        @param identity:
        @param name:
        @param styles: the styles applied to this node
        @param classes: the classes applied to this node
        """
        Comparable.__init__(self, identity, name)
        HasProperty.__init__(self)
        Stylable.__init__(
            self, styles, classes,
            add_default_styles=add_default_styles, add_default_classes=add_default_classes
        )

    def __str__(self):
        return 'Node(%s)' % self.identity

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def return_node(identity: Union[str, Node], styles: Iterable[Mapping] = (), classes: Iterable[str] = (),
                    add_default_styles: bool = False, add_default_classes: bool = False):
        if isinstance(identity, str):
            return Node(identity=identity, styles=styles, classes=classes,
                        add_default_styles=add_default_styles, add_default_classes=add_default_classes)
        elif isinstance(identity, Node):
            return identity
        else:
            raise TypeError(f'identity must be a string or a node instance. You gave {type(identity)}')


class NodeSet(ElementSet[Node]):
    def __init__(self, nodes: Iterable[Node]):
        """
        Create an edge set with a pile of elements.
        @param nodes:
        """
        super(NodeSet, self).__init__(nodes, Node)

    @staticmethod
    def generate_node_set(nodes: Iterable[Mapping]) -> Tuple[NodeSet, Mapping]:
        stored_nodes = {}
        all_has_id = all('id' in edge['data'] for edge in nodes)
        all_has_name = all('name' in edge['data'] for edge in nodes)

        if not (all_has_id or all_has_name) or (all_has_name and not all_has_id):
            raise GraphJsonFormatError('All Node entry must contain `name` and `id` fields or only `id` fields.')

        for node in nodes:
            if not (isinstance(node, Mapping) and 'data' in node):
                raise GraphJsonFormatError(f'invalid format for Node {node}')

            data_field = node['data']
            id_str = data_field['id']

            if all_has_name:
                name = data_field['name']
            else:
                name = id_str

            stored_node = Node(name)
            stored_node.cy_id = id_str

            if 'displayed' in data_field:
                stored_node.update_properties(data_field['displayed'])

            if name in stored_nodes:
                warnings.warn('Detected Duplicated Node in the graph.')

            stored_nodes[stored_node.cy_id] = stored_node

        return NodeSet(stored_nodes.values()), stored_nodes


class MutableNodeSet(NodeSet):
    def __init__(self, nodes: Iterable[Node] = ()):
        super().__init__(nodes)

    def add_node(self, *nodes: Node):
        if not all(isinstance(node, self.element_type) for node in nodes):
            raise TypeError(f'The Mutable Node Set Only Accept {self.element_type}')

        self.elements.update(nodes)

    def remove_node(self, *nodes: Node):
        if not all(isinstance(node, self.element_type) for node in nodes):
            raise TypeError(f'The Mutable Node Set Only Accept {self.element_type}')

        for node in nodes:
            self.elements.remove(node)
