from src.semantic.nodes.program import ProgramNode
from src.semantic.nodes.decl import VarDeclNode,FuncDeclNode

class SemVisitor:
    def __init__(self):
        pass
    
    def visit(self,node):
        return node.accept()
    
    def visit_program(self,program:ProgramNode):
        for i in program:
            self.visit(i)
    
    def visit_var_decl(self,var_decl:VarDeclNode):
        self.visit(var_decl.type)
        