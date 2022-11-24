from symbolTable import *
from VMWriter import *

# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
VMWriter = VMWriter('Planning/test.txt')

VMWriter.test('arithmetic', Command.NOT)
VMWriter.test('label', 'test')
VMWriter.test('push', Segments.ARG, 0)
VMWriter.test('pop', Segments.LOCAL, 0)
VMWriter.test('push', Segments.ARG, 1)
VMWriter.test('arithmetic', Command.NEG)
VMWriter.test('pop', Segments.LOCAL, 1)
