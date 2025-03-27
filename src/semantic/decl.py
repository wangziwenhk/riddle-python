from __future__ import annotations
from . import node
from . import stype
from . import expr

class VarDecl(node.SemNode):
    def __init__(self,name:str,typ:stype.TypeNode,value:expr.ExprNode):
        super().__init__()
        self.name = name
        self.type = typ
        self.value = value

class FuncDecl(node.SemNode):
    def __init__(self,name:str,typ:stype.TypeNode,param:list,body:list|None):
        super().__init__()
        self.name = name
        self.type = typ
        self.body = body
        self.param = param

    def delete_body(self):
        self.body = None