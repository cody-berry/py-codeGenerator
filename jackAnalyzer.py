from symbolTable import *
from VMWriter import *

# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
VMWriter = VMWriter('Planning/test.txt')

VMWriter.test('push')
