from symbolTable import *
from VMWriter import *

# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
VMWriter = VMWriter('Planning/test.txt')

symbolTable.define('test', 'yes?', VarType.FIELD)
symbolTable.define('another test', 'yes?', VarType.FIELD)
symbolTable.define('yet another test', 'yes?', VarType.FIELD)
symbolTable.define('the most common subroutine variable you\'ll ever see', 'yes?', VarType.FIELD)
symbolTable.define('test (2)', 'yes?', VarType.FIELD)
symbolTable.define('another test (2)', 'yes?', VarType.FIELD)
symbolTable.define('yet another test (2)', 'yes?', VarType.FIELD)
symbolTable.define('the most common subroutine variable you\'ll ever see (2)', 'yes?', VarType.FIELD)

print(symbolTable.kindOf('the most common subroutine variable you\'ll ever see (2)'))
print(symbolTable.typeOf('the most common subroutine variable you\'ll ever see (2)'))
print(symbolTable.indexOf('the most common subroutine variable you\'ll ever see (2)'))
