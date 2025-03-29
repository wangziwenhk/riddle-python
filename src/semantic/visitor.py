from typing import Optional

import antlr4

from src.parser.RiddleParser import RiddleParser
from src.parser.RiddleParserVisitor import RiddleParserVisitor
from .node import *
from .program import *
from .literal import *
from .decl import *
from .stype import BaseTypeNode, TypeNode


class GramVisitor(RiddleParserVisitor):
    def visitProgram(self, ctx: RiddleParser.ProgramContext):
        program = ProgramNode()
        for i in ctx.children:
            if not isinstance(i, antlr4.TerminalNode):
                program.add(self.visit(i))
        return program

    def visitPackStatement(self, ctx: RiddleParser.PackStatementContext):
        package = PackageNode(ctx.packName.getText())
        return package

    def visitInteger(self, ctx: RiddleParser.IntegerContext):
        return IntegerLiteralNode(ctx.value)

    def visitFloat(self, ctx: RiddleParser.FloatContext):
        return FloatLiteralNode(ctx.value)

    def visitBoolean(self, ctx: RiddleParser.BooleanContext):
        return BooleanLiteralNode(ctx.value)

    def visitVarDefineStatement(self, ctx: RiddleParser.VarDefineStatementContext):
        name = ctx.name.getText()
        value: Optional[expr.ExprNode] = None
        typ: Optional[stype.TypeNode] = None
        if ctx.value:
            value = self.visit(ctx.value)
        if ctx.type_:
            typ = self.visit(ctx.type_)
        elif ctx.value:
            typ = value.type

        return VarDeclNode(name, typ, value)

    def visitFuncDefine(self, ctx: RiddleParser.FuncDefineContext):
        name = ctx.funcName.getText()
        typ: Optional[stype.TypeNode]

        if ctx.returnType:
            typ = self.visit(ctx.returnType)
        else:
            typ = stype.BaseTypeNode.get_void()

        body = self.visit(ctx.body)

        func_decl = FuncDeclNode(name, typ, [], body)
        return func_decl

    def visitBodyExpr(self, ctx: RiddleParser.BodyExprContext):
        block: list[SemNode] = []
        for i in ctx.children:
            if not isinstance(i, antlr4.TerminalNode):
                block.append(self.visit(i))

        return block

    def visitBaseType(self, ctx:RiddleParser.BaseTypeContext):
        name = ctx.name.getText()
        if name in BaseTypeNode.BaseTypeEnum.__members__:
            return BaseTypeNode(name)
        else:
            return TypeNode(name)