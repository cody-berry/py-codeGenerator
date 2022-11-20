from symbolTable import *
from VMWriter import *

# from jackTokenizer import *
# from compilationEngine import *
# file = 'Average/Main.jack'
# tokenizer = JackTokenizer(file)
# compileEngine = CompilationEngine(file, tokenizer)
symbolTable = SymbolTable()
VMWriter = VMWriter('Planning/test.txt')
print(Segments.CONST, Segments.ARG, Segments.LOCAL, Segments.STATIC,
      Segments.THIS, Segments.THAT, Segments.POINTER, Segments.TEMP,
      Command.ADD, Command.SUB, Command.NEG, Command.EQ, Command.GT, Command.LT,
      Command.AND, Command.OR, Command.NOT)
print(VMWriter.output)
print(VMWriter.segmentEnumToVMSegmentMapping, VMWriter.commandEnumToVMArithmeticLogicCommandMapping)
