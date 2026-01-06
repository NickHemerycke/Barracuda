class varNode:

    def __init__(self, varType, name, valueNode):
        self.varType = varType
        self.name = name
        self.value = valueNode

class IfNode:
    def __init__(self, condition, then_branch):
        self.condition = condition
        self.then_branch = then_branch

class ReturnNode:
    def __init__(self, value):
        self.value = value
