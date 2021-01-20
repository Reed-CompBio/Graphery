from __future__ import annotations
from .Base import Stylable
from .Errors import GraphJsonFormatError
from .Node import Node, NodeSet, MutableNodeSet
from .Edge import Edge, EdgeSet, MutableEdgeSet, NodeTuple, EdgeIDTuple

import json
from typing import Iterable, Union, Optional, Mapping, Type, TypeVar, Generic
from enum import Enum


class GraphLayout(Enum):
    dagre = {'name': 'dagre'}
    fcose = {'name': 'fcose'}
    preset = {'name': 'preset'}
    random = {'name': 'random'}


_Node_C = TypeVar('_Node_C')
_Edge_C = TypeVar('_Edge_C')


class Graph(Stylable, Generic[_Node_C, _Edge_C]):
    """The graph object"""

    default_styles = [{
        "selector": "node",
        "style": {
            "label": "data(name)",
            "text-valign": "center",
            "text-halign": "center",
            "text-outline-color": "white",
            "text-outline-opacity": 1,
            "text-outline-width": 1,
            "height": "20px",
            "width": "20px",
            "font-size": "8px",
            "border-color": "black",
            "border-opacity": 1,
            "border-width": 1
        }
    }, ]

    def __init__(self, nodes: Iterable[Node], edges: Iterable[Edge],
                 node_container: Type[_Node_C] = NodeSet,
                 edge_container: Type[_Edge_C] = EdgeSet,
                 styles: Iterable[Mapping] = (), classes: Iterable[str] = (),
                 add_default_styles: bool = True,
                 add_default_classes: bool = True):
        """ graph constructor.

        @param nodes:
        @param edges:
        @raise ValueError: if nodes and edges are not iterable
        """
        super(Graph, self).__init__(
            styles, classes,
            add_default_styles=add_default_styles, add_default_classes=add_default_classes
        )

        if isinstance(nodes, Iterable) and isinstance(edges, Iterable):
            if isinstance(nodes, node_container):
                self.nodes = nodes
            else:
                self.nodes = node_container(nodes)
            if isinstance(edges, edge_container):
                self.edges = edges
            else:
                self.edges = edge_container(edges)
        else:
            raise ValueError

        self.V = self.nodes
        self.E = self.edges

        self.layout: Mapping = GraphLayout.dagre.value

        self.high_light_classes = []

    def get_node(self, node_id: str) -> Optional[Node]:
        """
        get a node by the node id
        @param node_id:
        @return: the node instance or None
        """
        return self.nodes[node_id]

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """
        get an edge by the edge id
        @param edge_id:
        @return: the edge instance or None
        """
        return self.edges[edge_id]

    def has_node(self, node: Union[str, Node]) -> bool:
        """
        Check if an node is in this graph
        @param node: a Node instance or the id of a node
        @return: boolean indicating the result
        """
        return node in self.nodes

    def has_edge(self, edge: Union[str, Edge]) -> bool:
        """
        Check if an edge is in this graph
        @param edge: an Edge instance or the id of an edge
        @return: boolean indicating the result
        """
        return edge in self.edges

    def empty(self) -> bool:
        return len(self.nodes) == 0

    def __contains__(self, item):
        """
        return true if the item is a node or an edge, and the item is in the graph
        @param item:
        @return:
        """
        if isinstance(item, Node):
            return self.has_node(item)
        elif isinstance(item, Edge):
            return self.has_edge(item)
        return False

    def set_layout(self, layout_name: GraphLayout) -> None:
        if isinstance(layout_name, GraphLayout):
            self.layout = layout_name.value
        else:
            print('Wrong layout name. Nothing is changed. Please use GraphLayout Enum.')

    @staticmethod
    def graph_generator(graph_json: Union[str, Mapping] = '') -> 'Graph':
        """
        generate a graph instance from json
        template:
        {
            elements: {
                nodes: [
                    {
                        data: { id: 'a', ..., displayed: { /* the properties that should tracked and displayed */}},
                        ...
                    },
                    ...
                ],
                edges: [
                    {
                        data: { id: 'ab', source: 'a', target: 'b', ...,
                                displayed: { /* the properties that should tracked and displayed */}
                              },
                        ...
                    },
                    ...
                ]
            },
            layout: { // omitted },
            style: [ { selector: '***', style: {'label': 'data(id)', ...}, ... ]
        }

        @param graph_json:
        @return: a graph instance built from the given json
        """
        # TODO this is not try enough, cut the json loading
        if isinstance(graph_json, str):
            try:
                graph_dict = json.loads(graph_json)
                # TODO do not support json5
            except TypeError as e:
                raise GraphJsonFormatError(e)
            except json.JSONDecodeError as e:
                raise GraphJsonFormatError('Please check the json format. '
                                           'The other json format is not supported for now. '
                                           f'Error: {e}')
        elif isinstance(graph_json, Mapping):
            graph_dict = graph_json
        else:
            raise GraphJsonFormatError('The graph json must be a json string or a json object')

        if 'elements' in graph_dict:
            element_dict = graph_dict['elements']
            layout_dict = graph_dict.get('layout', None)
            layout_name = GraphLayout(layout_dict) if layout_dict else GraphLayout.fcose
            if isinstance(element_dict, Mapping):
                parsed_node_set = []
                parsed_edge_set = []
                node_ids_instance_mapping = {}

                if 'nodes' in element_dict:
                    parsed_node_set, node_ids_instance_mapping = NodeSet.generate_node_set(element_dict['nodes'])

                if 'edges' in element_dict:
                    parsed_edge_set, edge_ids_instance_mapping = EdgeSet.generate_edge_set(element_dict['edges'],
                                                                                           node_ids_instance_mapping)

                g = Graph(parsed_node_set, parsed_edge_set)
                g.set_layout(layout_name)
                return g
        else:
            raise GraphJsonFormatError('malformed json file')


class MutableGraph(Graph):
    from .helpers import GraphObjectEncoder

    def __init__(self, nodes: Iterable[Node] = (), edges: Iterable[Edge] = ()):
        super().__init__(nodes, edges, node_container=MutableNodeSet, edge_container=MutableEdgeSet)

    def add_node(self, identity: Union[str, Node] = None,
                 styles: Union[str, Iterable[Mapping]] = (), classes: Iterable[str] = ()) -> Node:
        node = Node.return_node(identity=identity, styles=styles, classes=classes)
        self.nodes.add_node(node)
        return node

    def add_edge(self,
                 identity: str = None,
                 edge: Union[Edge, NodeTuple, EdgeIDTuple] = (),
                 styles: Union[str, Iterable[Mapping]] = (), classes: Iterable[str] = ()) -> Optional[Edge]:
        edge = Edge.return_edge(identity, edge, styles, classes)

        # TODO think about it
        for node in edge:
            self.add_node(node)

        self.edges.add_edge(edge)
        return edge

    def remove_node(self, identity: Union[str, Node], with_edge: bool = False) -> bool:
        node = Node.return_node(identity)
        related_edges = [edge for edge in self.edges if node in edge]
        if related_edges:
            if not with_edge:
                return False
            self.edges.remove_edge(*related_edges)

        self.nodes.remove_node(node)
        return True

    def remove_edge(self, identity: Union[str, Edge]) -> bool:
        # TODO it's a little messy here
        if isinstance(identity, Edge):
            edge = Edge.return_edge(edge=identity)
        else:
            edge = Edge.return_edge(identity=identity)

        self.edges.remove_edge(edge)
        return True

    def generate_json(self, indent: int = None) -> str:
        return json.dumps(self, indent=indent, cls=MutableGraph.GraphObjectEncoder)

    def generate_json_object(self) -> dict:
        return json.loads(self.generate_json())
