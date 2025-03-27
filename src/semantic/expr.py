from . import node
from . import stype

class ExprNode(node.SemNode):
    def __init__(self, typ:stype.TypeNode):
        super().__init__()
        self.type = typ
    