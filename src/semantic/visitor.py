import antlr4

from src.parser.RiddleParser import RiddleParser
from src.parser.RiddleParserVisitor import RiddleParserVisitor
from .program import ProgramNode
from .literal import IntegerLiteralNode, FloatLiteralNode, BooleanLiteralNode


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

    def visitBoolean(self, ctx):
        return BooleanLiteralNode(ctx.value)
    
    