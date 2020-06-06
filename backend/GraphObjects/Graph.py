import logging

from .Node import Node, NodeSet
from .Edge import Edge, EdgeSet
import json
from typing import Iterable, Union, Optional


class Graph:
    """
    The graph object
    """
    def __init__(self, nodes: Iterable[Node], edges: Iterable[Edge]):
        self.node_set = NodeSet(nodes)
        self.edge_set = EdgeSet(edges)
        self.high_light_classes = []

    def get_node(self, node_id: str) -> Optional[Node]:
        """
        get a node by the node id
        @param node_id:
        @return: the node instance or None
        """
        return self.node_set[node_id]

    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """
        get an edge by the edge id
        @param edge_id:
        @return: the edge instance or None
        """
        return self.edge_set[edge_id]

    def has_node(self, node: Union[str, Node]) -> bool:
        """
        Check if an node is in this graph
        @param node: a Node instance or the id of a node
        @return: boolean indicating the result
        """
        return self.node_set[node]

    def has_edge(self, edge: Union[str, Edge]) -> bool:
        """
        Check if an edge is in this graph
        @param edge: an Edge instance or the id of an edge
        @return: boolean indicating the result
        """
        return self.edge_set[edge]

    @staticmethod
    def graph_generator(graph_json: str = ''):
        """
        generate a graph instance from json
        template:
        {
            nodes: [
                {
                    data: { id: 'a', ... },
                    ...
                },
                ...
            ],
            edges: [
                {
                    data: { id: 'ab', source: 'a', target: 'b', ... },
                    ...
                },
                ...
            ]
            layout: { // omitted },
            style: [ { selector: '***', style: {'label': 'data(id)', ...}, ... ]
        }

        @param graph_json:
        @return: a graph instance built from the given json
        """
        try:
            graph_dict = json.loads(graph_json)
        except json.JSONDecodeError as e:
            logging.exception(e)
            raise e

        raise NotImplementedError

