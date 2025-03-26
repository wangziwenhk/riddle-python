from . import expr
from . import type


class IntegerLiteralNode(expr.ExprNode):
    def __init__(self, value: int):
        super().__init__(type.BaseTypeNode.get_int())
        self.value = value


class FloatLiteralNode(expr.ExprNode):
    def __init__(self, value: float):
        super().__init__(type.BaseTypeNode.get_float())
        self.value = value
