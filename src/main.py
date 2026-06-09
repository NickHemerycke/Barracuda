import sys
from lexer import lexBarracuda
from parser import Parser
from interpreter import Interpreter

if len(sys.argv) < 2:
    print("Usage: python main.py <path/to/file.cuda>")
    sys.exit(1)

with open(sys.argv[1]) as f:
    source = f.read()

tokens = lexBarracuda(source)
ast = Parser(tokens).parseProgram()
result = Interpreter().run(ast)
if result is not None:
    print(result)
