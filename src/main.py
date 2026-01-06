from lexer import lex_barracuda
from parser import Parser
from interpreter import Interpreter

source = open("test.cuda").read()

tokens = lex_barracuda(source)
ast = Parser(tokens).parse_program()

result = Interpreter().run(ast)
print(result)
