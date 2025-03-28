import llvmlite.ir as ir

from ..semantic.node import *
from ..semantic.program import *
from ..semantic.decl import *


class GenVisitor:
    def __init__(self):
        self.module = ir.Module()

    def visit_program(self, program: ProgramNode):
        for i in program:
            i.accept(self)

    def visit_package(self, package: PackageNode):
        self.module.name = package.name

    def visit_var_decl(self, var_decl: VarDeclNode):
        pass
