from . import expr
from . import stype


class IntegerLiteralNode(expr.ExprNode):
    def accept(self, visitor):
        return visitor.visit_integer(self)

    def __init__(self, value: int):
        super().__init__(stype.BaseTypeNode.get_int())
        self.value = value

    def __str__(self):
        return 'literal: ' + str(self.value)


class FloatLiteralNode(expr.ExprNode):
    def __init__(self, value: float):
        super().__init__(stype.BaseTypeNode.get_float())
        self.value = value

    def __str__(self):
        return 'literal: ' + str(self.value)

    def accept(self, visitor):
        return visitor.visit_float(self)


class BooleanLiteralNode(expr.ExprNode):
    def __init__(self, value: bool):
        super().__init__(stype.BaseTypeNode.get_bool())
        self.value = value

    def __str__(self):
        return 'literal: ' + str(self.value)

    def accept(self, visitor):
        return visitor.visit_boolean(self)