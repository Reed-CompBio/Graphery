import os.path

from bundle.GraphObjects.Edge import Edge
from bundle.GraphObjects.Node import Node

TEST_PATH = os.path.dirname(os.path.realpath(__file__))
path_join = os.path.join


def gen_edge(uid, id1, id2):
    return Edge(uid, (Node(id1), Node(id2)))
