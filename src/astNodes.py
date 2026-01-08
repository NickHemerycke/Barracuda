class varNode:

    def __init__(self, varType, name, valueNode):
        self.varType = varType
        self.name = name
        self.value = valueNode

class IfNode:
    def __init__(self, condition, thenBranch, elseBranch=None):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

class WhileNode:
    def __init__(self, condition,body):
        self.condition = condition
        self.body = body

#can't forget still gotta work on those just going crazy from seeing the none declare issue

class FuncNode:
    def __init__(self):
        return None

class ReturnNode:
    def __init__(self, value):
        self.value = value

class AssignNode:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr

class PrintNode:
    def __init__(self, value):
        self.value = value
