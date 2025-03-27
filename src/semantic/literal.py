from . import expr
from . import stype


class IntegerLiteralNode(expr.ExprNode):
    def __init__(self, value: int):
        super().__init__(stype.BaseTypeNode.get_int())
        self.value = value


class FloatLiteralNode(expr.ExprNode):
    def __init__(self, value: float):
        super().__init__(stype.BaseTypeNode.get_float())
        self.value = value

class BooleanLiteralNode(expr.ExprNode):
    def __init__(self, value:bool):
        super().__init__(stype.BaseTypeNode.get_bool())
        self.value = value

