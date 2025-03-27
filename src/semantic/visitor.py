import antlr4

from src.parser.RiddleParser import RiddleParser
from src.parser.RiddleParserVisitor import RiddleParserVisitor
from .program import ProgramNode
from .literal import IntegerLiteralNode, FloatLiteralNode, BooleanLiteralNode
from .decl import *


class GramVisitor(RiddleParserVisitor):
    def visitProgram(self, ctx: RiddleParser.ProgramContext):
        node = ProgramNode()
        for i in ctx.children:
            if not isinstance(i, antlr4.TerminalNode):
                node.add(self.visit(i))
        return node

    def visitInteger(self, ctx: RiddleParser.IntegerContext):
        return IntegerLiteralNode(ctx.value)

    def visitFloat(self, ctx: RiddleParser.FloatContext):
        return FloatLiteralNode(ctx.value)

    def visitBoolean(self, ctx: RiddleParser.BooleanContext):
        return BooleanLiteralNode(ctx.value)
    
    def visitVarDefineStatement(self, ctx: RiddleParser.VarDefineStatementContext):
        name = ctx.name.getText()
        value:expr.ExprNode | None = None
        type:stype.TypeNode | None = None
        if ctx.value:
            value = self.visit(ctx.value)
        if ctx.type_:
            type = self.visit(ctx.type_)
        elif ctx.value:
            type = value.type
        
        return VarDecl(name,type,value)
    
    def visitFuncDefine(self, ctx: RiddleParser.FuncDefineContext):
        name =  ctx.funcName.getText()
        return super().visitFuncDefine(ctx)