from symbolTable import *
# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
print(VarType.STATIC, VarType.FIELD, VarType.ARG, VarType.VAR, VarType.NONE)
print(symbolTable.classSymbolTable, symbolTable.subroutineSymbolTable, symbolTable.classLevelFieldCount, symbolTable.classLevelStaticCount, symbolTable.subroutineLevelArgCount, symbolTable.subroutineLevelLocalCount)
