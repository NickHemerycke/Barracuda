from lexer import lexBarracuda
from parser import Parser
from interpreter import Interpreter

document = "/home/nickhemerycke/Documents/projects/Insanity/Barracuda/tests/"
document = document + (input("Title of test document: "))


source = open(document).read()

tokens = lexBarracuda(source)
for t in tokens:
    print(t)
ast = Parser(tokens).parseProgram()

result = Interpreter().run(ast)
print(result)
