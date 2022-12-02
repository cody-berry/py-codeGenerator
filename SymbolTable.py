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
        # reset subroutine-level arg/local counts
        self.subroutineLevelLocalCount = 0
        self.subroutineLevelArgCount = 0

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

    # returns the number of variables that have a certain kind
    def varCount(self, kind):
        match kind:
            case VarType.STATIC:
                return self.classLevelStaticCount
            case VarType.FIELD:
                return self.classLevelFieldCount
            case VarType.ARG:
                return self.subroutineLevelArgCount
            case VarType.VAR:
                return self.subroutineLevelLocalCount

    # returns the kind of 'name', first searching through subroutine symbol
    # table before falling back to class symbol table
    def kindOf(self, name):
        for subroutineVar in self.subroutineSymbolTable:
            if subroutineVar['varName'] == name:
                return subroutineVar['kind']
        for classVar in self.classSymbolTable:
            if classVar['varName'] == name:
                return classVar['kind']
        return VarType.NONE

    # returns the type of 'name', first searching through subroutine symbol
    # table before falling back to class symbol table
    def typeOf(self, name):
        for subroutineVar in self.subroutineSymbolTable:
            if subroutineVar['varName'] == name:
                return subroutineVar['type']
        for classVar in self.classSymbolTable:
            if classVar['varName'] == name:
                return classVar['type']
        raise TypeError(f"Either {name} was not found as a variable, or it did not have a type.")

    # returns the index of 'name', first searching through subroutine symbol
    # table before falling back to class symbol table
    def indexOf(self, name):
        for subroutineVar in self.subroutineSymbolTable:
            if subroutineVar['varName'] == name:
                return subroutineVar['num']
        for classVar in self.classSymbolTable:
            if classVar['varName'] == name:
                return classVar['num']
        return IndexError(f"Either {name} was not found as a variable, or it did not have an index.")

