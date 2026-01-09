from astNodes import varNode, IfNode, ReturnNode, WhileNode, AssignNode, PrintNode

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.env = {}

    def evalExpression(self, node):
        kind = node[0]
        if kind == "BIN_OP":
            _, op, left, right = node
            leftValue = self.evalExpression(left)
            rightValue = self.evalExpression(right)

            if op == "+":
                return leftValue + rightValue
            elif op == "-":
                return leftValue - rightValue
            elif op == "===":
                return leftValue == rightValue
            elif op == "<":
                return leftValue < rightValue
            elif op == ">":
                return leftValue > rightValue
            elif op == "<=":
                return leftValue <= rightValue
            elif op == ">=":
                return leftValue >= rightValue
            elif op == "!=":
                return leftValue != rightValue
            else:
                raise ValueError(f"Unknown operator: {op}")

        elif kind == "NUM":
            return int(node[1])
        elif kind == "BOOL_VAL":
            return node[1] == "TRUE"
        elif kind == "ID":
            if node[1] in self.env:
                return self.env[node[1]]
            else:
                raise NameError(f"Variable '{node[1]}' not defined")
        else:
            raise ValueError(f"Unknown expression type: {kind}")


    def execVar(self, node):
        val = self.evalExpression(node.value)
        self.env[node.name] = val

    def execReturn(self, node):
        val = self.evalExpression(node.value)
        raise ReturnSignal(val)
    
    def execIf(self, node):
        if self.evalExpression(node.condition):
            for stmt in node.thenBranch:
                self.execStatement(stmt)
        elif node.elseBranch is not None:
            for stmt in node.elseBranch:
                self.execStatement(stmt)

    
    def execWhile(self,node):

        print("intiated while")
        
        while self.evalExpression(node.condition):
            for stmt in node.body:
                self.execStatement(stmt)

    def execAssign(self, node):
        if node.name not in self.env:
            raise NameError(f"Variable '{node.name}' not declared")
        value = self.evalExpression(node.expr)
        self.env[node.name] = value

    def execPrint(self, node):
        value = self.evalExpression(node.value)
        print(value)


    def execStatement(self, node):
        if isinstance(node, varNode):
            self.execVar(node)
        elif isinstance(node, IfNode):
            self.execIf(node)
        elif isinstance(node, WhileNode):
            self.execWhile(node)
        elif isinstance(node, ReturnNode):
            self.execReturn(node)
        elif isinstance(node, AssignNode):
            self.execAssign(node)
        elif isinstance(node, PrintNode):
            self.execPrint(node)

    def run(self, statements):
        try:
            for stmt in statements:
                self.execStatement(stmt)
        except ReturnSignal as r:
            return r.value
        
    






