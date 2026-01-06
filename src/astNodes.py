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
    def __init(self, condition):
        self.condition = condition

#can't forget still gotta work on those just going crazy from seeing the none declare issue

class FuncNode:
    def __init__(self):
        return None

class ReturnNode:
    def __init__(self, value):
        self.value = value
