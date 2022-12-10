from enum import Enum


class Segments(Enum):
    CONST = 0
    ARG = 1
    LOCAL = 2
    STATIC = 3
    THIS = 4
    THAT = 5
    POINTER = 6
    TEMP = 7


class Command(Enum):
    ADD = 0
    SUB = 1
    NEG = 2
    EQ = 3
    GT = 4
    LT = 5
    AND = 6
    OR = 7
    NOT = 8


class VMWriter:
    def __init__(self, output):
        self.output = open(output, 'w')
        # now we need to map the segment enums to VM segments
        self.segmentMapping = {
            Segments.CONST: 'constant',
            Segments.ARG: 'argument',
            Segments.LOCAL: 'local',
            Segments.STATIC: 'static',
            Segments.THIS: 'this',
            Segments.THAT: 'that',
            Segments.POINTER: 'pointer',
            Segments.TEMP: 'temp'
        }
        # plus, we need to map the command enums to VM arithmetic logic commands
        self.logicMapping = {
            Command.ADD: 'add',
            Command.SUB: 'sub',
            Command.NEG: 'neg',
            Command.EQ: 'eq',
            Command.GT: 'gt',
            Command.LT: 'lt',
            Command.AND: 'and',
            Command.OR: 'or',
            Command.NOT: 'not'
        }

    # writes a push command, or 'push segment index'. something like 'push arg 0'
    def writePush(self, segment, index):
        self.output.write('push ' + self.segmentMapping[segment] + ' ' + str(index) + '\n')

    # writes a pop command, or 'pop segment index'. something like 'pop local 0'
    def writePop(self, segment, index):
        self.output.write('pop ' + self.segmentMapping[segment] + ' ' + str(index) + '\n')

    # writes an arithmetic command, or 'command'. something like 'add'
    def writeArithmetic(self, command):
        self.output.write(self.logicMapping[command] + '\n')

    # writes a label command, or 'label labelName'. something like 'label L1'
    def writeLabel(self, labelName):
        self.output.write('label ' + labelName + '\n')

    # writes a goto command, or 'goto labelName'. something like 'goto L2'
    def writeGoto(self, labelName):
        self.output.write('goto ' + labelName + '\n')

    # writes an if-goto command, or 'if-goto labelName'. something like 'if-goto
    # L1'
    def writeIf(self, labelName):
        self.output.write('if-goto ' + labelName + '\n')

    # writes a call statement, or 'call functionName nArgs'. something like
    # 'call foo.bar 2'
    def writeCall(self, functionName, nArgs):
        self.output.write('call ' + functionName + ' ' + str(nArgs) + '\n')

    # writes a function statement, or the beginning of a function, or 'call
    # functionName nLocals'. something like 'function foo.bar 10'
    def writeFunction(self, functionName, nLocals):
        self.output.write('function ' + functionName + ' ' + str(nLocals) + '\n')

    # writes a return statement, or 'return'. this is the simplest as it
    # requires no arguments whatsoever. the assembly translation is very long,
    # though.
    def writeReturn(self):
        self.output.write('return\n')

    # tests all functions we've seen so far. it gives a function for testing
    # plus arg1 and arg2, which are possible arguments.
    def test(self, function, arg1=None, arg2=None):
        match function:
            case 'push':
                self.writePush(arg1, arg2)
            case 'pop':
                self.writePop(arg1, arg2)
            case 'arithmetic':
                self.writeArithmetic(arg1)
            case 'label':
                self.writeLabel(arg1)
            case 'goto':
                self.writeGoto(arg1)
            case 'if':
                self.writeIf(arg1)
            case 'call':
                self.writeCall(arg1, arg2)
            case 'fun':
                self.writeFunction(arg1, arg2)
            case 'return':
                self.writeReturn()















































































































































