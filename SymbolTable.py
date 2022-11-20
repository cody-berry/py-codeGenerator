from enum import Enum


# keeps track of all variable types we can store
class VarType(Enum):
    STATIC = 0
    FIELD = 1
    ARG = 2
    VAR = 3
    NONE = 4


class SymbolTable:
    def __init__(self):
        # we initialize our symbol tables
        self.classSymbolTable = []
        self.subroutineSymbolTable = []

        # then we keep track of the number of variables in each variable kind
        self.classLevelFieldCount = 0
        self.classLevelStaticCount = 0
        self.subroutineLevelArgCount = 0
        self.subroutineLevelLocalCount = 0

    # starts a subroutine
    def startSubroutine(self):
        # re-initialize subroutine symbol table
        self.subroutineSymbolTable = []

    # defines a new variable in the symbol table
    def define(self, name, varType, kind):
        newVar = {
            'varName': name,
            'type': varType,
            'kind': kind,
            'num': self.varCount(kind)
        }
        match kind:
            case VarType.STATIC:
                self.classSymbolTable.append(newVar)
                self.classLevelStaticCount += 1
            case VarType.FIELD:
                self.classSymbolTable.append(newVar)
                self.classLevelFieldCount += 1
            case VarType.ARG:
                self.subroutineSymbolTable.append(newVar)
                self.subroutineLevelArgCount += 1
            case VarType.VAR:
                self.subroutineSymbolTable.append(newVar)
                self.subroutineLevelLocalCount += 1

    def varCount(self, kind):
        return False
