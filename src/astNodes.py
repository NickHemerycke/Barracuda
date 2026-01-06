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

class ReturnNode:
    def __init__(self, value):
        self.value = value
