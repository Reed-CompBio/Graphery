from .Base import Highlightable, Comparable, HasProperty, Stylable, ElementSet
from typing import Iterable


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


class NodeSet(ElementSet):
    def __init__(self, nodes: Iterable[Node]):
        super(NodeSet, self).__init__(nodes, Node)
