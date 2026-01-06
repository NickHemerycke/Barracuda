from astNodes import varNode, IfNode, ReturnNode

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.env = {}

    def evalExpression(self, node):
        kind, value = node
        if kind == "NUM":
            return int(value)
        elif kind == "BOOL_VAL":
            return value == "TRUE"
        elif kind == "ID":
            if value in self.env:
                return self.env[value]
            else:
                raise NameError(f"Variable '{value}' not defined")
        else:
            raise ValueError(f"Unknown expression type: {kind}")


    def execVar(self, node):
        val = self.evalExpression(node.value)
        self.env[node.name] = val

    def execReturn(self, node):
        val = self.evalExpression(node.value)
        raise ReturnSignal(val)
    
    def execIf(self, node):
        left, _, right = node.condition

        conditionTrue = self.env[left] == self.evalExpression(right)

        if conditionTrue:
            for stmt in node.thenBranch:
                self.execStatement(stmt)
        elif node.elseBranch is not None:
            for stmt in node.elseBranch:
                self.execStatement(stmt)


    def execStatement(self, node):
        if isinstance(node, varNode):
            self.execVar(node)
        elif isinstance(node, IfNode):
            self.execIf(node)
        elif isinstance(node, ReturnNode):
            self.execReturn(node)

    def run(self, statements):
        try:
            for stmt in statements:
                self.execStatement(stmt)
        except ReturnSignal as r:
            return r.value
    






