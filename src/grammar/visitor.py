from typing import Optional

import antlr4

from src.parser.RiddleParser import RiddleParser
from src.parser.RiddleParserVisitor import RiddleParserVisitor
from src.semantic.nodes.node import *
from src.semantic.nodes.program import *
from src.semantic.nodes.literal import *
from src.semantic.nodes.decl import *
from src.semantic.nodes.stype import BaseTypeNode, TypeNode

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
                result = self.visit(i);
                if result is None:
                    continue
                block.append(result)

        return block

    def visitBaseType(self, ctx:RiddleParser.BaseTypeContext):
        name = ctx.name.getText()
        if name in BaseTypeNode.BaseTypeEnum.__members__:
            return BaseTypeNode(name)
        else:
            return TypeNode(name)
    
    def visitStatement_ed(self, ctx):
        return self.visit(ctx.children[0])
