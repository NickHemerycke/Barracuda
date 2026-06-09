from astNodes import varNode, IfNode, ReturnNode, WhileNode, FuncNode, FuncCallNode, AssignNode, PrintNode, BreakNode, ContinueNode

_COMPARISON_OPS = ("EQ", "NE", "ST", "GT", "STE", "GTE")
_BINARY_OPS     = ("PLUS", "MINUS") + _COMPARISON_OPS

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self, offset=0):
        idx = self.pos + offset
        if idx < len(self.tokens):
            return self.tokens[idx]
        return None

    def _skipNewlines(self):
        while self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

    def _parseBody(self, stopTokens=("DEDENT",)):
        body = []
        while True:
            self._skipNewlines()
            if not self.peek() or self.peek()[0] in stopTokens:
                break
            stmt = self.parseStatement()
            if stmt is not None:
                body.append(stmt)
        return body

    def consume(self, expected_type):
        token = self.peek()
        if token and token[0] == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Expected {expected_type}, got {token}")

    def parseProgram(self):
        statements = []
        while self.peek():
            stmt = self.parseStatement()
            if stmt is not None:
                statements.append(stmt)
        return statements

    def parseStatement(self):
        while self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        token = self.peek()
        if not token:
            return None

        if token[0] == "VAR":
            return self.parseVarDeclare()
        elif token[0] == "IF":
            return self.parseIfDeclare()
        elif token[0] == "WHILE":
            return self.parseWhileDeclare()
        elif token[0] == "FUNC":
            return self.parseFuncDeclare()
        elif token[0] == "ID" and self.peek(1) and self.peek(1)[0] == "ASSIGN":
            return self.parseAssignDeclare()
        elif token[0] == "PRINTLN":
            return self.parsePrintlnDeclare()
        elif token[0] == "BREAK":
            return self.parseBreak()
        elif token[0] == "CONT":
            return self.parseContinue()
        elif token[0] == "RET":
            return self.parseReturnDeclare()
        elif token[0] == "DEDENT":
            self.consume("DEDENT")
            return None
        else:
            return self.parseExpression()

    def parseExpression(self):
        token = self.peek()
        if not token or token[0] not in ("ID", "NUM", "BOOL_VAL"):
            raise SyntaxError(f"Expected expression, got {token}")
        self.pos += 1
        left = token

        # function call: ID followed by COLON
        if left[0] == "ID" and self.peek() and self.peek()[0] == "COLON":
            self.consume("COLON")
            args = [self.parseExpression()]
            while self.peek() and self.peek()[0] == "COMMA":
                self.consume("COMMA")
                args.append(self.parseExpression())
            return FuncCallNode(left[1], args)

        # binary operation
        if self.peek() and self.peek()[0] in _BINARY_OPS:
            op = self.consume(self.peek()[0])
            right = self.parseExpression()
            return ("BIN_OP", op[1], left, right)

        return left

    # var int x = 5
    def parseVarDeclare(self):
        self.consume("VAR")
        typeTok = self.consume("TYPE")
        nameTok = self.consume("ID")
        self.consume("ASSIGN")
        valueNode = self.parseExpression()
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        return varNode(typeTok[1], nameTok[1], valueNode)

    # if: x == 5
    #     ...
    def parseIfDeclare(self):
        self.consume("IF")
        self.consume("COLON")
        condition = self.parseExpression()

        while self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        self.consume("INDENT")
        thenBody = self._parseBody(stopTokens=("DEDENT", "ELSE"))
        if self.peek() and self.peek()[0] == "DEDENT":
            self.consume("DEDENT")

        elseBody = None
        if self.peek() and self.peek()[0] == "ELSE":
            self.consume("ELSE")
            self.consume("COLON")
            self._skipNewlines()
            self.consume("INDENT")
            elseBody = self._parseBody()
            if self.peek() and self.peek()[0] == "DEDENT":
                self.consume("DEDENT")

        return IfNode(condition=condition, thenBranch=thenBody, elseBranch=elseBody)

    # while: x < 5
    #     x = x + 1
    def parseWhileDeclare(self):
        self.consume("WHILE")
        self.consume("COLON")
        condition = self.parseExpression()

        while self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        self.consume("INDENT")
        body = self._parseBody()
        if self.peek() and self.peek()[0] == "DEDENT":
            self.consume("DEDENT")

        return WhileNode(condition, body)

    # x = expr
    def parseAssignDeclare(self):
        name = self.consume("ID")[1]
        self.consume("ASSIGN")
        expr = self.parseExpression()
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        return AssignNode(name, expr)

    # func: name: a, b, c
    #     ...
    def parseFuncDeclare(self):
        self.consume("FUNC")
        self.consume("COLON")
        name = self.consume("ID")[1]
        self.consume("COLON")

        args = [self.consume("ID")[1]]
        while self.peek() and self.peek()[0] == "COMMA":
            self.consume("COMMA")
            args.append(self.consume("ID")[1])

        while self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        self.consume("INDENT")
        body = self._parseBody()
        if self.peek() and self.peek()[0] == "DEDENT":
            self.consume("DEDENT")

        return FuncNode(name, args, body)

    # return: expr
    def parseReturnDeclare(self):
        self.consume("RET")
        self.consume("COLON")
        valueNode = self.parseExpression()
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        return ReturnNode(valueNode)
    

    def parseBreak(self):
        self.consume("BREAK")
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        return BreakNode()

    def parseContinue(self):
        self.consume("CONT")
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        return ContinueNode()

    # println: expr
    def parsePrintlnDeclare(self):
        self.consume("PRINTLN")
        self.consume("COLON")
        valueNode = self.parseExpression()
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        return PrintNode(valueNode)
