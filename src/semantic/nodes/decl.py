from typing import Optional
from .node import *
from .stype import *
from .expr import *
import llvmlite.ir as ir


class AllocaNode(SemNode):
    def __init__(self, typ: TypeNode):
        super().__init__()
        self.type = typ
        self.alloca: Optional[ir.AllocaInstr] = None

    def accept(self, visitor):
        return visitor.visit_alloca(self)

    def set_alloca(self, alloca: ir.AllocaInstr) -> None:
        self.alloca = alloca


class VarDeclNode(SemNode):
    def __init__(self, name: str, typ: TypeNode, value: ExprNode):
        super().__init__()
        self.name = name
        self.type = typ
        self.value = value
        self.alloca_node = AllocaNode(typ)

    def __str__(self):
        return f"varDecl:[name: {self.name}, {self.type}, {self.value}]"

    def accept(self, visitor):
        return visitor.visit_var_decl(self)


class FuncDeclNode(SemNode):
    def __init__(self, name: str, typ: TypeNode, param: list, body: Optional[list]):
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
