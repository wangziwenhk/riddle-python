import llvmlite.ir as ir

from ..semantic.node import *
from ..semantic.program import *
from ..semantic.decl import *
from ..semantic.stype import *
from .managers import *


class GenVisitor:
    def __init__(self):
        self.module = ir.Module()
        self.builder = ir.IRBuilder()
        self.object_manager = ObjectManager()
        self.base_type: dict[str, ir.Type] = {
            "int": ir.IntType(32),
            "float": ir.FloatType(),
            "double": ir.DoubleType(),
            "void": ir.VoidType(),
            "char": ir.IntType(8),
            "short": ir.IntType(16),
            "long": ir.IntType(64),
        }

    def visit(self, nod):
        return nod.accept(self)

    def visit_program(self, program: ProgramNode):
        self.object_manager.push()
        for i in program:
            i.accept(self)
        self.object_manager.pop()

    def visit_package(self, package: PackageNode):
        self.module.name = package.name

    def visit_func_decl(self, decl: FuncDeclNode):
        func = Function(decl.name, [], decl.type, decl.body)
        llvm_func_type = ir.FunctionType(self.visit(decl.type), [], False)
        llvm_func = ir.Function(self.module, llvm_func_type, decl.name)
        func.set_llvm_func(llvm_func)
        entry = llvm_func.append_basic_block("entry")

        self.builder = ir.IRBuilder(entry)
        self.object_manager.push()
        for i in decl.body:
            i.accept(self)
        self.object_manager.pop()

    def visit_var_decl(self, decl: VarDeclNode):
        var = Variable(decl.name, decl.type)
        self.visit(decl.type)
        alloca = self.builder.alloca(self.visit(decl.type))
        var.set_alloca(alloca)
        self.object_manager.add(decl.name, var)

    def visit_type(self, typ: TypeNode) -> ir.Type:
        if isinstance(typ, BaseTypeNode):
            if typ.name in self.base_type:
                return self.base_type[typ.name]
            else:
                raise TypeError(typ.name)

        return ir.VoidType()