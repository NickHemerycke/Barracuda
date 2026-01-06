from lexer import lexBarracuda
from parser import Parser
from interpreter import Interpreter
 

source = open("/home/nickhemerycke/Documents/projects/Insanity/Barracuda/tests/test.cuda").read()

tokens = lexBarracuda(source)
for t in tokens:
    print(t)
ast = Parser(tokens).parseProgram()

result = Interpreter().run(ast)
print(result)
