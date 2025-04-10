import antlr4
import os

from src.parser.RiddleParser import RiddleParser
from src.parser.RiddleLexer import RiddleLexer
from src.grammar.visitor import GramVisitor
from src.gen.visitor import GenVisitor

if __name__ == '__main__':
    file_path = "test/main.red"
    input_stream = antlr4.FileStream(file_path)
    lexer = RiddleLexer(input_stream)
    stream = antlr4.CommonTokenStream(lexer)
    parser = RiddleParser(stream)
    tree = parser.program()

    visitor = GramVisitor()
    result = visitor.visit(tree)
    gen = GenVisitor()
    gen.visit(result)
    print(gen.module)