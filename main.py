from lexer.lexer import Lexer
from parser.parser import Parser
from parser.ast_printer import ASTPrinter
from semantic.analyzer import SemanticAnalyzer
from ir.generator import IRGenerator
from vm.vm import VirtualMachine
import sys

with open(sys.argv[1], "r") as f:
    source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()

parser = Parser(tokens)
ast = parser.parse()

# printer = ASTPrinter()
# printer.print(ast)

semantic = SemanticAnalyzer()
semantic.analyze(ast)
# semantic.scope.table.dump()

generator = IRGenerator()
ir = generator.generate(ast)
# ir.dump()

vm = VirtualMachine()
vm.run(ir.instructions)