from symbolTable import *
from VMWriter import *

# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
VMWriter = VMWriter('Planning/test.txt')

symbolTable.subroutineSymbolTable = ['NEEDS TO BE RESET']
symbolTable.startSubroutine()

print(symbolTable.subroutineSymbolTable)
