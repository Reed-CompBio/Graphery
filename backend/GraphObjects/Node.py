from .Base import Highlightable, Hashable


class Node(Highlightable, Hashable):
    def __init__(self, identity, name, style):
        Hashable.__init__(identity, name)
        self.style = style

    def highlight(self, color):
        pass

    def unhighlight(self, color):
        pass