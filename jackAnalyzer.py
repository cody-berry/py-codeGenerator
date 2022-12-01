from jackTokenizer import *
from compilationEngine import *
file = 'Square/Square.jack'
tokenizer = JackTokenizer(file)
compileEngine = CompilationEngine(file, tokenizer)

print(compileEngine.symbolTable.subroutineSymbolTable)
print(compileEngine.symbolTable.classSymbolTable)

