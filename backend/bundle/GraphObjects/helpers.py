from __future__ import annotations
import json
from typing import Any, List

from .Base import HasProperty
from .Node import Node, NodeSet
from .Edge import Edge, EdgeSet
from .Graph import Graph

# TODO add default styles
default_directed_styles: dict = {}


class GraphObjectEncoder(json.JSONEncoder):
    @classmethod
    def displayed_encoding_added(cls, encoded: dict, obj: HasProperty) -> dict:
        encoded['data']['displayed'] = obj.properties
        return encoded

    @classmethod
    def return_node_encoding(cls, node: Node) -> dict:
        return cls.displayed_encoding_added(
            {
                'data': {
                    'id': node.cy_id,
                    'name': node.identity
                },
                'style': [node.styles],
            },
            node
        )

    @classmethod
    def return_edge_encoding(cls, edge: Edge) -> dict:
        return cls.displayed_encoding_added(
            {
                'data': {
                    'id': edge.cy_id,
                    'name': edge.identity,
                    'source': edge.get_incident_node().cy_id,
                    'target': edge.get_final_node().cy_id
                },
                'style': [
                    edge.styles,
                    default_directed_styles if edge.directed else {}
                ]
            },
            edge
        )

    @classmethod
    def return_node_set_encoding(cls, node_set: NodeSet) -> List[dict]:
        return [cls.return_node_encoding(node) for node in node_set]

    @classmethod
    def return_edge_set_encoding(cls, edge_set: EdgeSet) -> List[dict]:
        return [cls.return_edge_encoding(edge) for edge in edge_set]

    @classmethod
    def return_graph_encoding(cls, graph: Graph) -> dict:
        return {
            'elements': {
                'nodes': cls.return_node_set_encoding(graph.V),
                'edges': cls.return_edge_set_encoding(graph.E)
            },
            'style': [
                *graph.styles
            ],
            'layout': graph.layout
        }

    def default(self, obj: Any) -> Any:
        if isinstance(obj, Node):
            return self.return_node_encoding(obj)
        elif isinstance(obj, Edge):
            return self.return_edge_encoding(obj)
        elif isinstance(obj, NodeSet):
            return self.return_node_set_encoding(obj)
        elif isinstance(obj, EdgeSet):
            return self.return_edge_set_encoding(obj)
        elif isinstance(obj, Graph):
            return self.return_graph_encoding(obj)
        else:
            return json.JSONEncoder.default(self, obj)
