from . import node

class ExprNode(node.SemNode):
    def __init__(self, typ):
        super().__init__()
        self.type = typ
    