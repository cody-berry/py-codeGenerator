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
