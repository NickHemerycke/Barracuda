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
        
        valueNode = self.parse_expression() 
    
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")
        
        return varNode(typeTok[1], nameTok[1], valueNode)
    
    def parseFuncDeclare(self):

        self.consume("FUNC")

        self.consume("COLON")

        nameTok = self.consume("ID")

        self.consume("COLON")

        args = []

        args.append(self.consume("ID)[1]"))

        while self.peek() and self.peek()[0] == "COMMA":
            self.consume("COMMA")
            args.append(self.consume("ID")[1])

        self.consume("NEWLINE")

        
        self.consume("INDENT")
        body_nodes = []
        
        
        while self.peek() and self.peek()[0] != "DEDENT":
            
            node = self.parse_statement() 
            body_nodes.append(node)

        self.consume("DEDENT")

    
        return FuncNode(name=nameTok[1], arguments=args, body=body_nodes)
    
    def parseIfStatement(self):
        self.consume("IF")
        self.consume("COLON")

        # 1. Parse the condition
        left = self.consume("ID")
        op = self.consume("ASSIGN")
        right = self.parse_expression()

        # 2. Handle the gap between the condition and the body
        # Sometimes there's a NEWLINE before the INDENT
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        self.consume("INDENT")

        # 3. Parse the body
        if_body = []
        while self.peek() and self.peek()[0] != "DEDENT":
            # If we hit a stray newline inside the body, just skip it
            if self.peek()[0] == "NEWLINE":
                self.consume("NEWLINE")
                continue
            
            stmt = self.parse_statement()
            if stmt:
                if_body.append(stmt)
        
        # 4. Finish the block
        if self.peek() and self.peek()[0] == "DEDENT":
            self.consume("DEDENT")
            
        return IfNode(condition=(left[1], op[1], right), then_branch=if_body)

    def parseWhileLoop(self):
        
        self.consume("WHILE")
        self.consume("COLON")

        condition = self.parse_expression()
    
        self.consume("NEWLINE")
        self.consume("INDENT")
        
        body = []
        # Collect everything inside the tabbed block
        while self.peek() and self.peek()[0] != "DEDENT":
            body.append(self.parse_statement())
            
        self.consume("DEDENT")
        return WhileNode(condition=condition, body=body)
    

    def parse_statement(self):
        token = self.peek()
        if not token: return None
        
        if token[0] == "VAR":
            return self.parseVarDeclare()
        elif token[0] == "IF":
            return self.parseIfStatement()
        elif token[0] == "NEWLINE":
            self.consume("NEWLINE")
            return self.parse_statement() # Skip newline and find next statement
        else:
            # Fallback for now
            return self.parse_expression()  
        
    def parseIfStatement(self):
        self.consume("IF")
        self.consume("COLON")

        # 1. Parse the condition
        left = self.consume("ID")
        op = self.consume("ASSIGN")
        right = self.parse_expression()

        # 2. Handle the gap between the condition and the body
        # Sometimes there's a NEWLINE before the INDENT
        if self.peek() and self.peek()[0] == "NEWLINE":
            self.consume("NEWLINE")

        self.consume("INDENT")

        # 3. Parse the body
        if_body = []
        while self.peek() and self.peek()[0] != "DEDENT":
            # If we hit a stray newline inside the body, just skip it
            if self.peek()[0] == "NEWLINE":
                self.consume("NEWLINE")
                continue
            
            stmt = self.parse_statement()
            if stmt:
                if_body.append(stmt)
        
        # 4. Finish the block
        if self.peek() and self.peek()[0] == "DEDENT":
            self.consume("DEDENT")
            
        return IfNode(condition=(left[1], op[1], right), then_branch=if_body)

    def parse_expression(self):
        # This is a very basic version for now
        left = self.consume_any(['ID', 'NUM', 'BOOL_VAL'])
        
        # Check if there is math/comparison happening (e.g., +, -, ==, <)
        next_tok = self.peek()
        if next_tok and next_tok[0] in ['PLUS', 'MINUS', 'ASSIGN']: # Add PLUS/MINUS to Lexer!
            op = self.consume(next_tok[0])
            right = self.parse_expression() # Recursively find the rest
            return BinaryOpNode(left, op, right)
        
        return left # Just a single value
    
# Helper to consume any one of the types in a list
    def consume_any(self, types):
        token = self.peek()
        if token and token[0] in types:
            self.pos += 1
            return token
        else:
            raise SyntaxError(f"Expected one of {types}, got {token}")

    # The missing parse_expression function
    def parse_expression(self):
        # For now, this just handles a single ID, NUM, or BOOL
        # We can add math (BinaryOp) next
        return self.consume_any(['ID', 'NUM', 'BOOL_VAL'])

    

class varNode:
    def __init__(self, varType, name, value_node):
        self.varType = varType   # e.g., "int"
        self.name = name         # e.g., "outcome"
        self.value = value_node  # This will be another Node!
    def __repr__(self):
        return f"VarNode({self.varType} {self.name} = {self.value})"

class BinaryOpNode:
    def __init__(self, left, operator, right):
        self.left = left         # e.g., variable 'a'
        self.operator = operator # e.g., '-'
        self.right = right       # e.g., variable 'b'

class FuncNode:
    def __init__(self, name, arguments, body):
        self.name = name         
        self.arguments = arguments 
        self.body = body  
    def __repr__(self):
        return f"FuncNode(name={self.name}, args={self.arguments}, body={self.body})"         

class IfNode:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition  # This holds the (left, op, right) tuple
        self.then_branch = then_branch 
        self.else_branch = else_branch

    def __repr__(self):
        return f"IfNode(cond={self.condition}, then={self.then_branch})"

class WhileNode:
    def __init__(self, condition, body):
        
        self.condition = condition 
        self.body = body
    def __repr__(self):
        return f"WhileNode(cond={self.condition}, body={self.body})"
    
class ReturnNode:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"ReturnNode({self.value})"