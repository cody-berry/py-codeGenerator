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
        self.segmentEnumToVMSegmentMapping = {
            Segments.CONST: 'constant',
            Segments.ARG: 'arg',
            Segments.LOCAL: 'local',
            Segments.STATIC: 'static',
            Segments.THIS: 'this',
            Segments.THAT: 'that',
            Segments.POINTER: 'pointer',
            Segments.TEMP: 'temp'
        }
        # plus, we need to map the command enums to VM arithmetic logic commands
        self.commandEnumToVMArithmeticLogicCommandMapping = {
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
        self.output.write('push ' + self.segmentEnumToVMSegmentMapping[segment] + ' ' + str(index) + '\n')

    # writes a pop command, or 'pop segment index'. something like 'pop local 0'
    def writePop(self, segment, index):
        self.output.write('pop ' + self.segmentEnumToVMSegmentMapping[segment] + ' ' + str(index) + '\n')

    # writes an arithmetic command, or 'command'. something like 'add'.
    def writeArithmetic(self, command):
        self.output.write(self.commandEnumToVMArithmeticLogicCommandMapping[command] + '\n')

    # writes a label command, or 'label labelName'. something like 'label L1'.
    def writeLabel(self, labelName):
        self.output.write('label ' + labelName + '\n')

    # writes a goto command, or 'goto labelName'. something like 'goto L1'.
    def writeGoto(self, labelName):
        self.output.write('goto ' + labelName + '\n')

    def writeIf(self, labelName):
        self.output.write('if-goto ' + labelName + '\n')

    # tests all functions we've seen so far. it gives a function for testing plus arg1 and arg2, which are possible arguments.
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















































































































































