from symbolTable import *
from VMWriter import *

# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
VMWriter = VMWriter('Planning/test.txt')

symbolTable.define('test', 'yes?', VarType.VAR)
symbolTable.define('another test', 'yes?', VarType.ARG)
symbolTable.define('yet another test', 'yes?', VarType.STATIC)
symbolTable.define('the most common class variable you\'ll ever see', 'yes?', VarType.FIELD)

print(symbolTable.subroutineSymbolTable)
print(symbolTable.classSymbolTable)
