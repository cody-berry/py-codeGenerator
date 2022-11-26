from symbolTable import *
from VMWriter import *

# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
VMWriter = VMWriter('Planning/test.txt')

VMWriter.test('fun', 'foo.bar', 2)
VMWriter.test('push', Segments.ARG, 0)
VMWriter.test('push', Segments.ARG, 1)
VMWriter.test('arithmetic', Command.GT)
VMWriter.test('arithmetic', Command.NOT)
VMWriter.test('if-goto', 'L2')
VMWriter.test('label', 'L1')
VMWriter.test('push', Segments.ARG, 1)
VMWriter.test('pop', Segments.LOCAL, 0)
VMWriter.test('push', Segments.ARG, 2)
VMWriter.test('arithmetic', Command.NEG)
VMWriter.test('pop', Segments.LOCAL, 1)
VMWriter.test('goto', 'L3')
VMWriter.test('label', 'L2')
VMWriter.test('push', Segments.ARG, 1)
VMWriter.test('push', Segments.ARG, 2)
VMWriter.test('call', 'foo.add', 2)
VMWriter.test('pop', Segments.LOCAL, 0)
VMWriter.test('push', Segments.LOCAL, 0)
VMWriter.test('arithmetic', Command.NEG)
VMWriter.test('pop', Segments.LOCAL, 1)
VMWriter.test('label', 'L3')
VMWriter.test('return')

