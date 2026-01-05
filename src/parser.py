class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def consume(self, expected_type):
        token = self.peek()
        if token and token[0] == expected_type:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected {expected_type}, got {token}")
        

    def parseVarDeclare(self):

        self.consume("VAR")

        typeTok = self.consume("TYPE")

        nameTok = self.consume("ID")

        self.consume("ASSIGN")

        valTok = self.consume("NUM")

        return varNode(typeTok[1],nameTok[1],valTok[1])
    

class varNode:
    def __init__(self, varType, name, value):
        self.varType = varType
        self.name = name
        self.value = value

