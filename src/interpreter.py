class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.env = {}

    def evalExpression(self, node):
        kind, value = node

    def execVar(self, node):
        val = self.evalExpression(node.value)
        self.env[node.name] = val

    def execReturn(self, node):
        val = self.evalExpression(node.value)
        raise ReturnSignal(val)
    
    def execIf(self, node):
        left, _, right = node.condition
        if self.env[left] == self.evalExpression(right):
            for stmt in node.thenBranch:
                self.execStatement(stmt)

    def exec_statement(self, node):
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
    
    main()






