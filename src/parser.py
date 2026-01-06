from astNodes import varNode, IfNode, ReturnNode

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
        

    def parseProgram(self):
        statements = []
        while self.peek():
            statements.append(self.parseStatement())
        return statements
    
    def parseStatement(self):
        token = self.peek()

        if token[0] == "VAR":
            return self.parseVarDeclare()
        elif token[0] == "IF":
            return self.parseIfDeclare()
        elif token[0] == "WHILE":
            return self.parseWhileDeclare()
        elif token[0] == "FUNC":
            return self.parseFuncDeclare()
        elif token[0] == "RET":
            return self.parseReturnDeclare()
        elif token[0] == "NEWLINE":
            self.consume("NEWLINE")
            return self.parseStatement()
        elif token[0] == "DEDENT":
            return None
        else:
            return self.parseExpression()
        
    def parseExpression(self):

        token = self.peek()
        if token[0] in ("ID", "NUM", "BOOL_VAL"):
            self.pos += 1
            return token
        raise SyntaxError(f"Expected expression, got {token}")
        
        
#grammar section

    #example of var declarion is "var int x == 5"
        
    def parseVarDeclare(self):
        self.consume("VAR")
        typeTok = self.consume("TYPE")
        nameTok = self.consume("ID")
        self.consume("ASSIGN")
        
        valueNode = self.parseExpression() 
    
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        
        return varNode(typeTok[1], nameTok[1], valueNode)
    

    """example of if statement is " if: x == 5"
                                       var int y == 6
    """

    def parseIfDeclare(self):
        self.consume("IF")
        self.consume("COLON")

        left = self.consume("ID")
        self.consume("ASSIGN")
        right = self.parseExpression()

        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        self.consume("INDENT")

        body = []
        while self.peek() and self.peek()[0] != "DEDENT":
            stmt = self.parseStatement()
            if stmt is not None:
                body.append(stmt)

        self.consume("DEDENT")

        return IfNode(
            condition=(left[1], "==", right),
            thenBranch=body
        )

    
    """example of a while statement is " while: x < 5"
                                            x = x + 1
    """
    
    def parseWhileDeclare(self):
        self.consume("WHILE")
        self.consume("COLON")

        condition = self.parseExpression()

        self.consume("INDENT")

        body = []
        while self.peek()[0] != "DEDENT":
            body.append(self.parseStatement())

        self.consume("DEDENT")

        return WhileNode(condition, body)
    

    def parseFuncDeclare(self):
        self.consume("FUNC")
        self.consume("COLON")

        name = self.consume("ID")[1]

        self.consume("COLON")

        args = [self.consume("ID")[1]]
        while self.peek()[0] == "COMMA":
            self.consume("COMMA")
            args.append(self.consume("ID")[1])

        self.consume("INDENT")

        body = []
        while self.peek()[0] != "DEDENT":
            body.append(self.parseStatement())

        self.consume("DEDENT")

        return FuncNode(name, args, body)
    
    def parseReturnDeclare(self):
        self.consume("RET")
        valueNode = self.parseExpression()

        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        return ReturnNode(valueNode)
    


