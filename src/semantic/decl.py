from __future__ import annotations
from . import node
from . import stype
from . import expr


class VarDeclNode(node.SemNode):
    def __init__(self, name: str, typ: stype.TypeNode, value: expr.ExprNode):
        super().__init__()
        self.name = name
        self.type = typ
        self.value = value

    def __str__(self):
        return f"varDecl:[name: {self.name}, {self.type}, {self.value}]"

    def accept(self, visitor):
        return visitor.visit_var_decl(self)


class FuncDeclNode(node.SemNode):
    def __init__(self, name: str, typ: stype.TypeNode, param: list, body: list | None):
        super().__init__()
        self.name = name
        self.type = typ
        self.body = body
        self.param = param

    def delete_body(self):
        self.body = None

    def __str__(self):
        body_temp = [] if self.body is None else [str(item) for item in self.body]
        return f'funcDecl:[name: {self.name},body: {body_temp}]'

    def accept(self, visitor):
        return visitor.visit_func_decl(self)