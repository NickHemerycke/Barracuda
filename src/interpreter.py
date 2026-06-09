from astNodes import varNode, IfNode, ReturnNode, WhileNode, FuncNode, FuncCallNode, AssignNode, PrintNode

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class Interpreter:
    def __init__(self):
        self.env = {}
        self.funcs = {}

    def evalExpression(self, node):
        if isinstance(node, FuncCallNode):
            if node.name not in self.funcs:
                raise NameError(f"Function '{node.name}' not defined")
            func = self.funcs[node.name]
            if len(node.args) != len(func.args):
                raise TypeError(f"'{node.name}' expects {len(func.args)} args, got {len(node.args)}")
            arg_values = [self.evalExpression(a) for a in node.args]
            return self.callFunc(func, arg_values)

        kind = node[0]
        if kind == "BIN_OP":
            _, op, left, right = node
            lv = self.evalExpression(left)
            rv = self.evalExpression(right)
            if op == "+":  return lv + rv
            if op == "-":  return lv - rv
            if op == "==": return lv == rv
            if op == "!=": return lv != rv
            if op == "<":  return lv < rv
            if op == ">":  return lv > rv
            if op == "<=": return lv <= rv
            if op == ">=": return lv >= rv
            raise ValueError(f"Unknown operator: {op}")
        elif kind == "NUM":
            return int(node[1])
        elif kind == "BOOL_VAL":
            return node[1] == "TRUE"
        elif kind == "ID":
            if node[1] in self.env:
                return self.env[node[1]]
            raise NameError(f"Variable '{node[1]}' not defined")
        else:
            raise ValueError(f"Unknown expression type: {kind}")

    def execVar(self, node):
        val = self.evalExpression(node.value)
        if node.varType == "int":
            if not isinstance(val, int) or isinstance(val, bool):
                raise TypeError(f"'{node.name}' declared as int but got {type(val).__name__}")
        elif node.varType == "bool":
            if not isinstance(val, bool):
                raise TypeError(f"'{node.name}' declared as bool but got {type(val).__name__}")
        self.env[node.name] = val

    def execIf(self, node):
        if self.evalExpression(node.condition):
            for stmt in node.thenBranch:
                self.execStatement(stmt)
        elif node.elseBranch is not None:
            for stmt in node.elseBranch:
                self.execStatement(stmt)

    def execWhile(self, node):
        while self.evalExpression(node.condition):
            for stmt in node.body:
                self.execStatement(stmt)

    def execFunc(self, node):
        self.funcs[node.name] = node

    def callFunc(self, func_node, arg_values):
        saved_env = self.env
        self.env = dict(saved_env)
        for param, val in zip(func_node.args, arg_values):
            self.env[param] = val
        try:
            for stmt in func_node.body:
                self.execStatement(stmt)
            return None
        except ReturnSignal as r:
            return r.value
        finally:
            self.env = saved_env

    def execAssign(self, node):
        self.env[node.name] = self.evalExpression(node.expr)

    def execReturn(self, node):
        raise ReturnSignal(self.evalExpression(node.value))

    def execPrint(self, node):
        print(self.evalExpression(node.value))

    def execStatement(self, node):
        if isinstance(node, varNode):
            self.execVar(node)
        elif isinstance(node, IfNode):
            self.execIf(node)
        elif isinstance(node, WhileNode):
            self.execWhile(node)
        elif isinstance(node, FuncNode):
            self.execFunc(node)
        elif isinstance(node, ReturnNode):
            self.execReturn(node)
        elif isinstance(node, AssignNode):
            self.execAssign(node)
        elif isinstance(node, PrintNode):
            self.execPrint(node)
        elif isinstance(node, FuncCallNode):
            self.evalExpression(node)

    def run(self, statements):
        try:
            for stmt in statements:
                self.execStatement(stmt)
        except ReturnSignal as r:
            return r.value
